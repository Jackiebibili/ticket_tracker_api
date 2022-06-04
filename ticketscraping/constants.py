from uuid import uuid4
from urllib.parse import quote_plus

ANTIBOT_JS_CODE_URL = "https://epsf.ticketmaster.com/eps-d"
TOKEN_INTERROGATION_URL = "https://epsf.ticketmaster.com/eps-d?d=www.ticketmaster.com"


def get_top_picks_url(
    eventId): return f"https://offeradapter.ticketmaster.com/api/ismds/event/{eventId}/quickpicks"


EVENT_ID = "0C005B5587A017CF"
BASIC_REQ_HEADER = {"origin": "https://www.ticketmaster.com",
                    "referer": "https://www.ticketmaster.com/"}
def get_top_picks_header(): return {
    **BASIC_REQ_HEADER,
    "tmps-correlation-id": str(uuid4())
}

def get_top_picks_query_params_str(qty=2, priceInterval=(
    0, 100)):
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
    def encodeURI(s):
        return quote_plus(s, safe="():=,$@'")
    def formulateURI(params):
        items = []
        for p in params:
            if isinstance(params[p], list):
                for i in params[p]:
                    items.append(encodeURI(f"{p}={i}"))
            else:
                items.append(encodeURI(f"{p}={params[p]}"))
        return '?' + '&'.join(items)
    return formulateURI(get_top_picks_query_params(qty, priceInterval))

FN_MATCHING_REGEX = r"\(function\(\){.*}\)\(\)"
TOKEN_RENEW_SEC_OFFSET = 3
TOKEN_RENEW_PRIORITY = 3
TICKET_SCRAPING_PRIORITY = 1
TICKET_SCRAPING_INTERVAL = 60

INJECTOR_LOCATION = "js/injector.js"
INJECTOR_HEADER_LOCATION = "js/injector-header.js"
RENNABLE_FILENAME = "js/antibot-simulation.js"
