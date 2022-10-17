class Pick():
   def __init__(self, type, selection, quality, section, row, area, maxQuantity, offer, seat_columns, _id=None, scraping_id=None):
      self._id = _id
      self.scraping_id = scraping_id
      self.type = type
      self.selection = selection
      self.quality = quality
      self.section = section
      self.row = row
      self.area = area
      self.maxQuantity = maxQuantity
      self.offer = offer
      self.price = offer.get('listPrice')
      self.seat_columns = seat_columns
   
   def setScrapingId(self, scraping_id: str):
      self.scraping_id = scraping_id

   def __eq__(self, other):
      return (self.section == other.section and self.row == other.row and
              ((type(self.seat_columns) is list and len(
                  self.seat_columns) > 0 and type(other.seat_columns) is list and len(
                  other.seat_columns) > 0 and self.seat_columns[0] == other.seat_columns[0]) or 
                  (self.seat_columns is None and other.seat_columns is None)) and
               self.price == other.price)

   def __hash__(self):
      return hash((self.section,
                   self.row,
                   self.seat_columns[0] if type(self.seat_columns) is list and len(
                       self.seat_columns) > 0 else None,
                   self.price))
