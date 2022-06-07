import os
import sched
import time
import json
import requests
import subprocess
from . import constants
from threading import Semaphore
from .prepare_reese84token import getReese84Token

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
        self.token_semaphore.release() # produce a new token
        self.scheduler.enter(self.reese84_token['renewInSec'] -
                             constants.TOKEN_RENEW_SEC_OFFSET, constants.TOKEN_RENEW_PRIORITY, self.renew_reese84_token)

    def renew_reese84_token(self):
        """
        This method should not be called directly.
        """
        self.token_semaphore.acquire() # invalidate a token
        self.reese84_token = getReese84Token()
        self.token_semaphore.release()
        self.scheduler.enter(self.reese84_token['renewInSec'] -
                             constants.TOKEN_RENEW_SEC_OFFSET, constants.TOKEN_RENEW_PRIORITY, self.renew_reese84_token)
    
    def start(self):
        # if the scheduler is already started - do nothing
        if self.is_running: return
        self.is_running = True
        self.initialize_reese84_token()
        self.scheduler.run(False)
    


class TicketScraping():
    def __init__(self, token_generator: Reese84TokenUpdating, event_id = constants.EVENT_ID, num_seats=2, price_range=(0, 200)):
        self.event_id = event_id
        self.num_seats = num_seats
        self.price_range = price_range
        self.token_gen = token_generator
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.is_running = False

    def ticket_scraping(self):
        if self.token_gen.token_semaphore._value <= 0:
            # retry after a delay
            self.scheduler.enter(constants.TICKET_SCRAPING_TOKEN_AWAIT_MAX_INTERVAL,
                                 constants.TICKET_SCRAPING_PRIORITY, self.ticket_scraping)
            return
        top_picks_url = constants.get_top_picks_url(self.event_id)
        top_picks_q_params = constants.get_top_picks_query_params(
            self.num_seats, self.price_range)
        top_picks_header = constants.get_top_picks_header()
        res = requests.get(top_picks_url, headers=top_picks_header, params=top_picks_q_params,
                           cookies=dict(reese84=self.token_gen.reese84_token['token']))
        print(res.json())
        self.scheduler.enter(constants.TICKET_SCRAPING_INTERVAL,
                  constants.TICKET_SCRAPING_PRIORITY, self.ticket_scraping)
    
    def start(self):
        # if the scheduler is already started - do nothing
        if self.is_running:
            return
        self.is_running = True
        self.ticket_scraping()
        self.scheduler.run(False)


def start():
    reese_token_gen = Reese84TokenUpdating()
    ticket_scraping = TicketScraping(reese_token_gen)
    reese_token_gen.start()
    ticket_scraping.start()
