from ....storage.storage import count_docs, find_many
from ....ticketscraping import constants
from ...models.pick import Pick


def price_decrease_similar_rank(pick: Pick, scraping_id: str):
    filter_obj = {
        "scraping_id": scraping_id,
        "price": {"$gt": pick.price},
        "quality": {"$lte": pick.quality},
    }
    count = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj)
    seats = find_many(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj, sort=[
                      ("quality", -1)]) if count > 0 else None
    return (count, seats)


def price_increase_similar_rank(pick: Pick, scraping_id: str):
    filter_obj = {
        "scraping_id": scraping_id,
        "price": {"$lt": pick.price},
        "quality": {"$gte": pick.quality},
    }
    count = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj)
    seats = find_many(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj, sort=[
                      ("quality", 1)]) if count > 0 else None
    return (count, seats)
