import pymongo
from ....storage.storage import count_docs, find_many
from ....storage.query import find_max, find_min, find_many_ascending_order
from ....ticketscraping import constants
from ...models.pick import Pick
from ..util.math import percentile


class QuartersSeats():
    top_better_history_seats_sort = [
        ('rank', pymongo.DESCENDING), ('price', pymongo.ASCENDING)]

    def __init__(self, pick: Pick, scraping_id: str, target_price: int):
        self._pick = pick
        self._scraping_id = scraping_id
        self.target_price = target_price
        self.percentile = 1.0

    def __lt__(self, other):
        # smaller the percentile, better the pick
        return self.percentile > other.percentile

    def __eq__(self, other):
        return self.percentile == other.percentile

    @property
    def pick(self):
        return self._pick

    @property
    def scraping_id(self):
        return self._scraping_id

    def get_alert_content(self):
        # alert user
        # Find the exact same seat based on(sec, row?, seat?)
        same_seats = self.get_exact_same_seats()
        # rank = self._num_before + 1
        # top best history = get_top_better_history_seats()
        # notify user with info
        return ''
        pass

    def get_top_better_history_seats(self):
        return self.find_better_history_seats(sort=self.top_better_history_seats_sort)

    def shouldAlert(self):
        try:
            # Find price match
            self.target_price_metric()
            # Find enough history seats data
            percentile = self.percentile_metric()
            # Find the % of change
            percent_change = self.percent_of_change_metric()
            # Find percentile of seats in quarters
            self.quarter_percentile_metric()
        except Exception as ex:
            print(ex)
            return False

        # success
        print(f"percent change out of max-min: {percent_change*100}")
        print(f"all history seats percentile: {percentile*100}")
        print(
            f"new seat - price: {self.pick.price} rank: {self.pick.quality} section: {self.pick.section} row: {self.pick.row}")
        print(f"quarters history seats percentile: {self.percentile*100}")
        return True


    def quarter_percentile_metric(self):
        if self.get_percentile() > constants.PERCENTILE_HISTORY_PRICES:
            raise Exception('the seat is not recommended')

    def get_percentile(self):
        self._num_before = self.count_better_history_seats()
        self._num_total = self.count_quarters_history_seats()
        self.percentile = percentile(self._num_before, self._num_total)
        return self.percentile

    def count_quarters_history_seats(self):
        filter_obj = self.__get_quarters_history_seats_filter__()
        return count_docs(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj)

    def __get_quarters_history_seats_filter__(self):
        return {
            "scraping_id": self._scraping_id,
            "$or": [
               {
                   "price": {"$lte": self._pick.price},
                   "quality": {"$gte": self._pick.quality},
               },
                {
                   "price": {"$gt": self._pick.price},
                   "quality": {"$lt": self._pick.quality},
               }
            ]
        }

    def __get_better_history_seats_filter__(self):
        return {
            "scraping_id": self._scraping_id,
            "$or": [
               {
                   "price": {"$lt": self._pick.price},
                   "quality": {"$gte": self._pick.quality},
               },
                {
                   "price": {"$lte": self._pick.price},
                   "quality": {"$gt": self._pick.quality},
               }
            ]
        }

    def find_better_history_seats(self, **kwargs):
        limit = kwargs.get('limit')
        sort_seq = kwargs.get('sort')
        filter_obj = self.__get_better_history_seats_filter__()
        return find_many(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj, sort=sort_seq, limit=limit)

    def count_better_history_seats(self):
        filter_obj = self.__get_better_history_seats_filter__()
        return count_docs(constants.DATABASE['BEST_HISTORY_SEATS'], filter_obj)
    
    def target_price_metric(self):
        # exceed target price - abort
        if self.pick.price > self.target_price:
            raise Exception('price of the seat is not low enough')


    def percent_of_change_metric(self) -> float:
        # Find the % of change
        max_seat = find_max(constants.DATABASE['BEST_HISTORY_SEATS'], {
            "scraping_id": self.scraping_id}, 'price')
        min_seat = find_min(constants.DATABASE['BEST_HISTORY_SEATS'], {
            "scraping_id": self.scraping_id}, 'price')
        max_price = 0 if type(max_seat) is not dict else max_seat.get('price', 0)
        min_price = 0 if type(min_seat) is not dict else min_seat.get('price', 0)

        # min and max are identical - abort
        if max_price == min_price:
            raise Exception('min and max prices are identical')

        percent_change = (self.pick.price - min_price) / (max_price - min_price)

        # # price of change exceeds the metric value - abort
        # if percent_change > constants.PERCENT_OF_CHANGE:
        #     raise Exception(
        #         f'price of change ({percent_change}) exceeds the metric value')

        return percent_change


    def percentile_metric(self) -> float:
        rank = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                        {"scraping_id": self.scraping_id, "price": {"$lte": self.pick.price}})
        total_count = count_docs(constants.DATABASE['BEST_HISTORY_SEATS'],
                                {
            "scraping_id": self.scraping_id})

        # no history seats data - abort
        if total_count < constants.MINIMUM_HISTORY_DATA:
            raise Exception('no enough history seats data (count < 3)')

        percentile = rank / total_count

        # # percentile of history prices exceeds the metric value - abort
        # if percentile > constants.PERCENTILE_HISTORY_PRICES:
        #     raise Exception(
        #         'percentile of history prices ({percentile}) exceeds the metric value')

        return percentile


    def get_exact_same_seats(self):
        return find_many_ascending_order(constants.DATABASE['BEST_HISTORY_SEATS'],
                                        {"scraping_id": self.scraping_id, "section": self.pick.section,
                                        "row": self.pick.row, "seat_columns": self.pick.seat_columns},
                                        'last_modified')
