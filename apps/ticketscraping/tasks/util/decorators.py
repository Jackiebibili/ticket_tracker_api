class StorageInsertionOrder:
   def __init__(self, size=0):
      self.store = [0] * size

   def __iter__(self):
      return iter(self.store)

   @property
   def size(self):
      return len(self.store)

   def add(self, item):
      self.store.append(item)

   def get(self, index: int):
      return self.store[index]

   def set(self, index: int, item):
      self.store[index] = item

   def sort(self):
      sorted(self.store)
   
   def filter(self):
      self.store = list(filter(lambda item: item is not None, self.store))

   def sublist(self, from_idx: int, to_idx: int):
      return self.store[from_idx:to_idx]


def wrap_fn_return(fn, storing_fn, index):
   def inner_fn(*args, **kwargs):
      res = fn(*args, **kwargs)
      storing_fn(index, res)
      return res
   return inner_fn