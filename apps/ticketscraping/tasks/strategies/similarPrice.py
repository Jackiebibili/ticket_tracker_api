from ....storage.storage import count_docs
from ....ticketscraping import constants
from ...models.pick import Pick


def rank_increase_similar_price(pick: Pick, scraping_id: str):
    return count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                      {
        "scraping_id": scraping_id,
        "price": {"$gte": pick.price},
        "quality": {"$lt": pick.quality},
    }) > 0


def rank_decrease_similar_price(pick: Pick, scraping_id: str):
    return count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                      {
        "scraping_id": scraping_id,
        "price": {"$lte": pick.price},
        "quality": {"$gt": pick.quality},
    }) > 0
