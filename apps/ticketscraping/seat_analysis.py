from dateutil import parser
from ..storage.storage import insert_one
from ..ticketscraping import constants


def store_seats(data, scheduler_config):
    # prune top-picks data structure
    pruned_picks = prune_pick_attributes(data)

    # process seats data - use piping
    res = pipe([
        append_scraping_config_ref,
        map_prices_to_seats,
        remove_embedded_field
    ], pruned_picks, scheduler_config)

    # store in db
    # print(res)
    insert_one(constants.DATABASE['TOP_PICKS'], res)
    pass

def pipe(fns: list, *args):
    out = args
    for fn in fns:
        if type(out) is tuple:
            out = fn(*out)
        else:
            out = fn(out)
    return out


def prune_pick_attributes(data):
    def prune_pick_offer_attributes(pick):
        return {
            'type': pick['type'],
            'selection': pick['selection'],
            'quality': pick['quality'],
            'section': pick['section'],
            'row': pick['row'],
            'offerGroups': pick['offerGroups'],
            'area': pick['area'],
            'maxQuantity': pick['maxQuantity'],
        }

    def prune_pick_embedded_attributes(embedded):
        def prune_pick_embedded_offer_attributes(item):
            return {
                'expired_date': parser.parse(item['meta']['expires']),
                'offerId': item['offerId'],
                'rank': item['rank'],
                'online': item['online'],
                'protected': item['protected'],
                'rollup': item['rollup'],
                'inventoryType': item['inventoryType'],
                'offerType': item['offerType'],
                'currency': item['currency'],
                'listPrice': item['listPrice'],
                'faceValue': item['faceValue'],
                'totalPrice': item['totalPrice'],
                'noChargesPrice': item['noChargesPrice'],
               #  'listingId': item['listingId'],
               #  'listingVersionId': item['listingVersionId'],
               #  'charges': item['charges'],
               #  'sellableQuantities': item['sellableQuantities'],
               #  'section': item['section'],
               #  'row': item['row'],
               #  'seatFrom': item['seatFrom'],
               #  'seatTo': item['seatTo'],
               #  'ticketTypeId': item['ticketTypeId']
            }
        return {
            'offer': list(map(prune_pick_embedded_offer_attributes, embedded['offer']))
        }
    return {
        'expired_date': parser.parse(data['meta']['expires']),
        'eventId': data['eventId'],
        'offset': data['offset'],
        'total': data['total'],
        'picks': list(map(prune_pick_offer_attributes, data['picks'])),
        '_embedded': prune_pick_embedded_attributes(data['_embedded'])
    }


def append_scraping_config_ref(data, scheduler_config):
    data['scraping_config_ref'] = scheduler_config
    return data


def map_prices_to_seats(data):
    def map_prices_to_seat_helper(offer_table: dict):
        def __map_prices_to_seat_helper(pick):
            offerGroups = pick['offerGroups']
            offerGroup = offerGroups[0]
            offerIds = offerGroup['offers']
            offerSeatCols = offerGroup['seats']
            if len(offerGroups) == 0 or len(offerIds) == 0:
                return {'offer_available': False}
            offerId = offerIds[0]
            offerObj = offer_table.get(offerId)
            res = {**pick, 'offer': offerObj, 'seat_columns': offerSeatCols}
            del res['offerGroups']
            return res
        return __map_prices_to_seat_helper
    offer_dict = {offer['offerId']: offer for offer in data['_embedded']['offer']}
    picks_list = list(
        map(map_prices_to_seat_helper(offer_dict), data['picks']))
    data['picks'] = picks_list
    return data

def remove_embedded_field(data):
    del data['_embedded']
    return data
