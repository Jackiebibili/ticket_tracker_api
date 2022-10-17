from ...storage.storage import count_docs
from ...storage.query import find_max, find_min, find_many_ascending_order
from ...ticketscraping import constants
from ..models.pick import Pick

# metric 1


def percent_of_change_metric(pick: Pick, scraping_id: str) -> float:
    # Find the % of change
    max_seat = find_max(constants.DATABASE['BEST_HISTORY_SEATS'], {
        "scraping_id": scraping_id}, 'price')
    min_seat = find_min(constants.DATABASE['BEST_HISTORY_SEATS'], {
        "scraping_id": scraping_id}, 'price')
    max_price = max_seat.get('price', 0)
    min_price = min_seat.get('price', 0)

    # min and max are identical - abort
    if max_price == min_price:
        raise Exception('min and max prices are identical')

    percent_change = (pick.price - min_price) / (max_price - min_price)

    # price of change exceeds the metric value - abort
    if percent_change > constants.PERCENT_OF_CHANGE:
        raise Exception(
            f'price of change ({percent_change}) exceeds the metric value')

    return percent_change

# metric 2


def percentile_metric(pick: Pick, scraping_id: str) -> float:
    rank = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                      {"scraping_id": scraping_id, "price": {"$lte": pick.price}})
    total_count = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                             {
        "scraping_id": scraping_id})

    # no history seats data - abort
    if total_count == 0:
        raise Exception('no history seats data')

    percentile = rank / total_count

    # percentile of history prices exceeds the metric value - abort
    if percentile > constants.PERCENTILE_HISTORY_PRICES:
        raise Exception(
            'percentile of history prices ({percentile}) exceeds the metric value')

    return percentile


def get_exact_same_seats(pick: Pick, scraping_id: str):
    return find_many_ascending_order(constants.DATABASE['BEST_HISTORY_SEATS'],
                                     {"scraping_id": scraping_id, "section": pick.section,
                                      "row": pick.row, "seat_columns": pick.seat_columns},
                                     'last_modified')


def run_async_task(pick: Pick, scraping_id: str):
    try:
        # Find the % of change
        percent_change = percent_of_change_metric(pick, scraping_id)
        # Find the percentile of the seat based on some criteria(e.g. rank or price).
        percentile = percentile_metric(pick, scraping_id)
        # If found the exact same seat based on(sec, row?, seat?), get the history price(s) of the seat.
        same_seats = get_exact_same_seats(pick, scraping_id)

        print(f"percent change: {percent_change*100}")
        print(f"percentile: {percentile*100}")
        print(f"same seats in chronological order")
        print(f"new seat price: {pick.price}")
        print(f"history seat prices:")
        print(list(map(lambda seat: seat.get('price', -1), same_seats)))

        # TODO
        # Alert the user based on alert conditions

    except Exception as ex:
        print(ex)
    pass
