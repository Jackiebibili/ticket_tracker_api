from ...storage.storage import find_many, insert_many, delete_many
from ...ticketscraping import constants
from ..models.pick import Pick
from .asynchronous import run_async_task

def generate_picks_set_from_picks(picks):
   def __helper(pick: dict):
      return Pick(_id=pick.get('_id'),
                  scraping_id=pick.get('scraping_id'),
                  type=pick['type'],
                  selection=pick['selection'],
                  quality=pick['quality'],
                  section=pick['section'],
                  row=pick['row'],
                  area=pick['area'],
                  maxQuantity=pick['maxQuantity'],
                  offer=pick['offer'],
                  seat_columns=pick['seat_columns'])

   if type(picks) is dict:
      return set(map(__helper, picks['picks']))
   elif type(picks) is list:
      return set(map(__helper, picks))
   else:
      raise Exception('argument type error')

def get_current_best_available(scraping_id: str):
   return find_many(constants.DATABASE['BEST_AVAILABLE_SEATS'], {"scraping_id": scraping_id})
def remove_best_seats(seats: set[Pick]):
   ids = []
   for seat in seats:
      ids.append(seat._id)
   return delete_many(constants.DATABASE['BEST_AVAILABLE_SEATS'], {"_id" : {"$in": ids}})
def insert_best_seats(seats: set[Pick], scraping_id: str):
   for seat in seats:
      seat.setScrapingId(scraping_id)
   return insert_many(constants.DATABASE['BEST_AVAILABLE_SEATS'], list(map(lambda seat: vars(seat), seats)))
def insert_history_seats(seats: set[Pick]):
   return insert_many(constants.DATABASE['BEST_HISTORY_SEATS'], list(map(lambda seat: vars(seat), seats)))



def run_periodic_task(picks: dict, scraping_id: str):
   # B the list of new best available seats
   new_best_avail = generate_picks_set_from_picks(picks)
   # A be the list of current best available seats
   cur_best_avail = generate_picks_set_from_picks(get_current_best_available(scraping_id))

   # Compute C := A-B which is the seats
   overwritten_seats = cur_best_avail - new_best_avail

   # Compute D := B-A which is the new seats
   new_seats = new_best_avail - cur_best_avail

   print(f"size of B is {len(new_best_avail)}")
   print(f"size of A is {len(cur_best_avail)}")
   print(f"size of C is {len(overwritten_seats)}")
   print(f"size of D is {len(new_seats)}")
   
   # Remove C from best_available_seats
   remove_best_seats(overwritten_seats)

   # Insert D to best_available_seats
   insert_best_seats(new_seats, scraping_id)

   # Save C to best_history_seats.
   insert_history_seats(overwritten_seats)

   # Use D to invoke a handler to analyze them against the best_history_seats asynchronously.
   for seat in new_seats:
      run_async_task(seat, scraping_id)
   pass