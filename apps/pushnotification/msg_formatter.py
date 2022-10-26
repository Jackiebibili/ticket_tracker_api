from datetime import datetime
from ..ticketscraping.models.pick import Pick

def price_formatter(price):
   price_str = ''
   if type(price) is float or int:
      price_str = "$" + "{:.2f}".format(price)
   elif type(price) is str:
      price_str = price
   return price_str

def decimal_to_percent(num: float):
   return "{:.2f}".format(num*100) + "%"

def format_date(date: datetime):
   return date.isoformat()

def default_formatter(s: str):
   return s

def format_seat_columns(cols):
   if type(cols) is str:
      return cols
   elif type(cols) is list:
      return "(" + ",".join(cols) + ")"
   return '-'

def apply_format(s, formatter)->str:
   return formatter(s)

def apply(values: list, formatters: list, delimiter="\t"):
   if len(values) != len(formatters):
      raise Exception('values and formatters must have the same length')
   s = []
   for i in range(len(values)):
      s.append(apply_format(values[i], formatters[i]))
   return delimiter.join(s)

def format_full_seat(seat: dict, delimiter="\t"):
   price = seat.get("price", "n/a")
   section = seat.get("section", "n/a")
   row = seat.get("row", "n/a")
   seat_columns = seat.get("seat_columns", "n/a")
   last_modified = seat.get("last_modified", "n/a")
   return apply(
      [price, section, row, seat_columns, last_modified],
      [price_formatter, default_formatter, default_formatter,
       format_seat_columns, format_date],
      delimiter)

def format_price_only_seat(seat: dict, delimiter="\t"):
   price = seat.get("price", "n/a")
   last_modified = seat.get("last_modified", "n/a")
   return apply([price, last_modified], [price_formatter, format_date], delimiter)

def format_seat(seat: dict, price_only=False, delimiter="\t"):
   if price_only:
      return format_price_only_seat(seat, delimiter)
   else:
      return format_full_seat(seat, delimiter)

def format_seats(seats: list, price_only=False, delimiter="\t"):
   return "\n".join([format_seat(seat, price_only, delimiter) for seat in seats])


def format_entire_mail(pick: Pick, target_price: int, percentile: float, rank: int, num_total: int, top_history_seats: list, same_seats: list):
    """
        structure of message:
         1. greetings
         2. attributes of new seats
         3. top 3 comparable history seats
         4. exact same seats if possible
         5. signature
   """
    p1 = (
        f"Hi!"
    )
    p2 = (
        f"Congratulations! Ticket tracker reminds you that your ticket subscription request with target price {price_formatter(target_price)} "
        f"found better budget seats (price, section, row, seats) at ({format_full_seat(vars(pick), delimiter=', ')}). "
        f"{decimal_to_percent(percentile)} of all comparable seats in the history are better than the newly found seats, that is, "
        f"they rank no.{rank} out of {num_total} comparable seats in the history."
    )
    p3 = (
        f"You can compare to history seats that are better than the newly found seats:"
        f"{chr(10)}"
        f"{format_seats(top_history_seats, price_only=False)}"
    ) if len(top_history_seats) > 0 else ""
    p4 = (
        f"The newly found seats have history prices:"
        f"{chr(10)}"
        f"{format_seats(same_seats, price_only=True)}"
    ) if len(same_seats) > 0 else ""
    p5 = (
        f"Bests,"
        f"{chr(10)}"
        f"Ticketmaster Ticket Tracker"
    )
    paras = list(filter(lambda p: len(p) > 0, [p1, p2, p3, p4, p5]))
    return "\n\n".join(paras)
