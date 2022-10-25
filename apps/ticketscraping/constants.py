from uuid import uuid4

ANTIBOT_JS_CODE_URL = "https://epsf.ticketmaster.com/eps-d"
TOKEN_INTERROGATION_URL = "https://epsf.ticketmaster.com/eps-d?d=www.ticketmaster.com"


def get_top_picks_url(
    eventId): return f"https://offeradapter.ticketmaster.com/api/ismds/event/{eventId}/quickpicks"


EVENT_ID = "0C005B5587A017CF"
BASIC_REQ_HEADER = {"origin": "https://www.ticketmaster.com",
                    "referer": "https://www.ticketmaster.com/"}
DATABASE = {
    "EVENTS": "events",
    "TOP_PICKS": "top-picks",
    "BEST_AVAILABLE_SEATS": "best-available-seats",
    "BEST_HISTORY_SEATS": "best-history-seats"
}
def get_top_picks_header(): return {
    **BASIC_REQ_HEADER,
    "tmps-correlation-id": str(uuid4())
}

def get_top_picks_query_params(qty, priceInterval): return {
    'show': 'places maxQuantity sections',
    'mode': 'primary:ppsectionrow resale:ga_areas platinum:all',
    'qty': qty,
    'q': f"and(not(\'accessible\'),any(listprices,$and(gte(@,{priceInterval[0]}),lte(@,{priceInterval[1]}))))",
    'includeStandard': 'true',
    'includeResale': 'true',
    'includePlatinumInventoryType': 'false',
    'embed': ['area', 'offer', 'description'],
    'apikey': 'b462oi7fic6pehcdkzony5bxhe',
    'apisecret': 'pquzpfrfz7zd2ylvtz3w5dtyse',
    'limit': 100,
    'offset': 0,
    'sort': '-quality',
}

FN_MATCHING_REGEX = r"\(function\(\){.*}\)\(\)"
TOKEN_RENEW_SEC_OFFSET = 3
TOKEN_RENEW_PRIORITY = 1
TICKET_SCRAPING_PRIORITY = 3
TICKET_SCRAPING_INTERVAL = 60
TICKET_SCRAPING_TOKEN_AWAIT_MAX_INTERVAL = 5

INJECTOR_LOCATION = "js/injector.js"
INJECTOR_HEADER_LOCATION = "js/injector-header.js"
RENNABLE_FILENAME = "js/antibot-simulation.js"
