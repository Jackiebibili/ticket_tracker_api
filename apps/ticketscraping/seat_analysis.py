from dateutil import parser
from ..storage.storage import insert_one
from ..ticketscraping import constants


def store_seats(data, subscriber_id):
    # prune top-picks data structure
    pruned_picks = prune_pick_attributes(data)

    # process seats data - use piping
    res = pipe([
        append_scraping_config_ref,
        map_prices_to_seats,
        remove_embedded_field
    ], pruned_picks, subscriber_id)

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

def get_value_from_map(map: dict, *args, **kwargs):
    # input validation
    if type(map) is not dict:
        return kwargs.get('default', None)
    res = kwargs.get('default', None)
    for attr in args:
        res = map.get(attr)
        if res is not None:
            break
    return res

def get_value_from_nested_map(map: dict, *args, **kwargs):
    # input validation
    if type(map) is not dict:
        return kwargs.get('default', None)
    res = None
    m = map
    count = 0
    for attr in args:
        res = m.get(attr)
        count += 1
        if res is None:
            break
        elif type(res) is dict:
            m = res
        else:
            break
    return res if res is not None and count == len(args) else kwargs.get('default', None)

def get_fn_return(fn, *args, **kwargs):
    res = kwargs.get('default', None)
    try:
        res = fn(*args)
    except:
        pass
    finally:
        return res

def prune_pick_attributes(data):
    def prune_pick_offer_attributes(pick: dict):
        return {
            'type': get_value_from_map(pick, 'type'),
            'selection': get_value_from_map(pick, 'selection'),
            'quality': get_value_from_map(pick, 'quality'),
            'section': get_value_from_map(pick, 'section'),
            'row': get_value_from_map(pick, 'row'),
            'offerGroups': get_value_from_map(pick, 'offerGroups', 'offers'),
            'area': get_value_from_map(pick, 'area'),
            'maxQuantity': get_value_from_map(pick, 'maxQuantity'),
        }

    def prune_pick_embedded_attributes(embedded: dict):
        def prune_pick_embedded_offer_attributes(item):
            return {
                'expired_date': get_fn_return(parser.parse, get_value_from_nested_map(item, 'meta', 'expires'), default=None),
                'offerId': get_value_from_map(item, 'offerId'),
                'rank': get_value_from_map(item, 'rank'),
                'online': get_value_from_map(item, 'online'),
                'protected': get_value_from_map(item, 'protected'),
                'rollup': get_value_from_map(item, 'rollup'),
                'inventoryType': get_value_from_map(item, 'inventoryType'),
                'offerType': get_value_from_map(item, 'offerType'),
                'currency': get_value_from_map(item, 'currency'),
                'listPrice': get_value_from_map(item, 'listPrice'),
                'faceValue': get_value_from_map(item, 'faceValue'),
                'totalPrice': get_value_from_map(item, 'totalPrice'),
                'noChargesPrice': get_value_from_map(item, 'noChargesPrice'),
               #  'listingId': get_value_from_map(item, 'listingId'),
               #  'listingVersionId': get_value_from_map(item, 'listingVersionId'),
               #  'charges': get_value_from_map(item, 'charges'),
               #  'sellableQuantities': get_value_from_map(item, 'sellableQuantities'),
               #  'section': get_value_from_map(item, 'section'),
               #  'row': get_value_from_map(item, 'row'),
               #  'seatFrom': get_value_from_map(item, 'seatFrom'),
               #  'seatTo': get_value_from_map(item, 'seatTo'),
               #  'ticketTypeId': get_value_from_map(item, 'ticketTypeId')
            }
        return {
            'offer': list(map(prune_pick_embedded_offer_attributes, get_value_from_map(embedded, 'offer', default=dict())))
        }
    return {
        'expired_date': get_fn_return(parser.parse, get_value_from_nested_map(data, 'meta', 'expires'), default=None),
        'eventId': get_value_from_map(data, 'eventId'),
        'offset': get_value_from_map(data, 'offset'),
        'total': get_value_from_map(data, 'total'),
        'picks': list(map(prune_pick_offer_attributes, get_value_from_map(data, 'picks', default=dict()))),
        '_embedded': prune_pick_embedded_attributes(get_value_from_map(data, '_embedded', default=dict()))
    }


def append_scraping_config_ref(data, config_id):
    data['scraping_config_ref'] = config_id
    return data


def map_prices_to_seats(data):
    def map_prices_to_seat_helper(offer_table: dict):
        def __map_prices_to_seat_helper(pick):
            offerGroups = pick['offerGroups']
            if offerGroups is None or len(offerGroups) == 0:
                return {'offer_available': False}
            offerGroup = offerGroups[0]
            offerIds = get_value_from_map(offerGroup, 'offers', default=[offerGroup])
            offerSeatCols = get_value_from_map(offerGroup, 'seats')
            if len(offerIds) == 0:
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
