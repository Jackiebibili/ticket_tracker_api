import os
import sched
import time
import json
import requests
import subprocess
from . import constants
from threading import Semaphore
from .prepare_reese84token import getReese84Token

s = sched.scheduler(time.time, time.sleep)
token_semaphore = Semaphore(1)
reese84_token = {}
    

def obtainReese84Token(sch):
    global reese84_token, token_semaphore
    token_semaphore.acquire()
    reese84_token = getReese84Token()
    token_semaphore.release()
    print(reese84_token)
    sch.enter(reese84_token['renewInSec'] -
              constants.TOKEN_RENEW_SEC_OFFSET, constants.TOKEN_RENEW_PRIORITY, obtainReese84Token, (sch,))


def ticket_scraping(sch):
    global reese84_token, token_semaphore
    token_semaphore.acquire()
    top_picks_url = constants.get_top_picks_url(constants.EVENT_ID)
    top_picks_q_params_str = constants.get_top_picks_query_params_str(2, (0, 200))
    top_picks_url = top_picks_url + top_picks_q_params_str
    top_picks_header = constants.get_top_picks_header()
    res = requests.get(top_picks_url, headers=top_picks_header,
                       cookies=dict(reese84=reese84_token['token']))
    token_semaphore.release()
    print(res.json())
    sch.enter(constants.TICKET_SCRAPING_INTERVAL,
              constants.TICKET_SCRAPING_PRIORITY, ticket_scraping, (sch,))

def start():
    obtainReese84Token(s)
    ticket_scraping(s)
    s.run()
