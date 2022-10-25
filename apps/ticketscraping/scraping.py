import sched
import time
import ctypes
import random
import requests
import threading
from . import constants
from threading import Semaphore
from .prepare_reese84token import getReese84Token
from ..storage.storage import *
from .seat_analysis import format_seats
from .tasks.periodic import run_periodic_task

class Reese84TokenUpdating():
    def __init__(self):
        self.is_running = False
        self.reese84_token = {}
        self.token_semaphore = Semaphore(0)
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def initialize_reese84_token(self):
        """
        This method should not be called directly.
        """
        self.reese84_token = getReese84Token()
        self.token_semaphore.release()  # produce a new token
        self.scheduler.enter(self.reese84_token['renewInSec'] -
                             constants.TOKEN_RENEW_SEC_OFFSET, constants.TOKEN_RENEW_PRIORITY, self.renew_reese84_token)

    def renew_reese84_token(self):
        """
        This method should not be called directly.
        """
        print("renewing token")
        self.token_semaphore.acquire()  # invalidate a token
        self.reese84_token = getReese84Token()
        self.token_semaphore.release()
        self.scheduler.enter(self.reese84_token['renewInSec'] -
                             constants.TOKEN_RENEW_SEC_OFFSET, constants.TOKEN_RENEW_PRIORITY, self.renew_reese84_token)

    def start(self):
        # if the scheduler is already started - do nothing
        if self.is_running:
            return
        self.is_running = True
        self.initialize_reese84_token()
        self.scheduler.run()


class TicketScraping(threading.Thread):
    def __init__(self, token_generator: Reese84TokenUpdating, event_id, subscribe_id, num_seats=2, price_range=(0, 200)):
        threading.Thread.__init__(self)
        self.is_running = False
        self.is_stopping = False
        self.event_id = event_id
        self.subscribe_id = subscribe_id
        self.num_seats = num_seats
        self.price_range = price_range
        self.token_gen = token_generator
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.initialDelay = random.randint(
            1, constants.TICKET_SCRAPING_INTERVAL)

    def flag_for_termination(self):
        # cancel all scheduled jobs
        list(map(self.scheduler.cancel, self.scheduler.queue))
        # raise exception to terminate the thread
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        print(
            f"Ticket scraping with subscription id={self.subscribe_id} marked for termination.")
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print(f'Failed to terminate the thread with id={thread_id}')

    def ticket_scraping(self):
        if self.token_gen.token_semaphore._value <= 0:
            # phase: retry after a delay
            self.scheduler.enter(constants.TICKET_SCRAPING_TOKEN_AWAIT_MAX_INTERVAL,
                                 constants.TICKET_SCRAPING_PRIORITY, self.ticket_scraping)
            return
        # scrape the top-picks from ticketmaster
        top_picks_url = constants.get_top_picks_url(self.event_id)
        top_picks_q_params = constants.get_top_picks_query_params(
            self.num_seats, self.price_range)
        top_picks_header = constants.get_top_picks_header()
        res = requests.get(top_picks_url, headers=top_picks_header, params=top_picks_q_params,
                           cookies=dict(reese84=self.token_gen.reese84_token['token']))
        # print(res.json())

        # prune and format the received picks
        picks_obj = format_seats(res.json(), self.subscribe_id)

        # periodic task: update collections best_available_seats and best_history_seats
        run_periodic_task(picks_obj, self.subscribe_id)

        print("Got the ticket info from TM. /", res.status_code)
        self.scheduler.enter(constants.TICKET_SCRAPING_INTERVAL,
                             constants.TICKET_SCRAPING_PRIORITY, self.ticket_scraping)

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def run(self):
        try:
            # if the scheduler is already started - do nothing
            if self.is_running:
                return
            self.is_running = True
            self.is_stopping = False
            self.ticket_scraping()
            # randomize start time to scatter out event of API fetching
            time.sleep(self.initialDelay)
            self.scheduler.run()
        finally:
            print(
                f"Ticket scraping with subscription id={self.subscribe_id} has been terminated.")


def start():
    # reese84 token renewing thread
    reese_token_gen = Reese84TokenUpdating()
    serverThread_reese = threading.Thread(target=reese_token_gen.start)
    serverThread_reese.start()

    # ticket scraping threads
    scraping_list = dict()
    events = find_many(constants.DATABASE["EVENTS"], {
                       '$or': [{'markPaused': {'$exists': False}}, {'markPaused': False}]})
    for evt in events:
        ticket_scraping = TicketScraping(
            reese_token_gen, evt["tm_event_id"], evt["_id"], evt["ticket_num"], evt["price_range"])
        print(ticket_scraping.initialDelay, "s")
        scraping_list[ticket_scraping.subscribe_id] = ticket_scraping
    for scraping_thread in scraping_list.values():
        scraping_thread.start()

    # listen for changes in ticket scraping subscriptions
    while(True):
        with watch(constants.DATABASE["EVENTS"], pipeline=[{'$match': {'operationType': {'$in': ['delete', 'insert', 'replace', 'update']}}}], full_document='updateLookup') as stream:
            for change in stream:
                if change['operationType'] == "delete":
                    # stop the thread
                    doc_id = change['documentKey']['_id']
                    if doc_id in scraping_list:
                        scraping_obj = scraping_list[doc_id]
                        scraping_obj.flag_for_termination()
                        del scraping_list[doc_id]
                elif change['operationType'] == "insert":
                    # spawn a thread to do scraping operations
                    full_doc = change['fullDocument']
                    ticket_scraping = TicketScraping(
                        reese_token_gen, full_doc["tm_event_id"], full_doc["_id"], full_doc["ticket_num"], full_doc["price_range"])
                    print(ticket_scraping.initialDelay, "s")
                    scraping_list[ticket_scraping.subscribe_id] = ticket_scraping
                    ticket_scraping.start()
                else:
                    # replace or update - pause or resume ticket scraping
                    full_doc = change['fullDocument']
                    doc_id = full_doc['_id']
                    if not 'markPaused' in full_doc:
                        print("'markPaused' flag is unset, skip processing.")
                        break
                    if full_doc['markPaused'] == True:
                        # pause scraping
                        if doc_id in scraping_list:
                            scraping_obj = scraping_list[doc_id]
                            scraping_obj.flag_for_termination()
                            del scraping_list[doc_id]
                    else:
                        # resume scraping if currently paused
                        if doc_id not in scraping_list:
                            ticket_scraping = TicketScraping(
                                reese_token_gen, full_doc["tm_event_id"], full_doc["_id"], full_doc["ticket_num"], full_doc["price_range"])
                            print(ticket_scraping.initialDelay, "s")
                            scraping_list[ticket_scraping.subscribe_id] = ticket_scraping
                            ticket_scraping.start()
                # display current number of ticket scraping
                print(f"{len(scraping_list)} ticket scraping threads now.")
