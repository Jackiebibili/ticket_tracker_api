from pymongo import collection

def __insert_one__(coll: collection.Collection, doc: dict):
   return coll.insert_one(doc)

def __insert_many__(coll: collection.Collection, docs: list):
   return coll.insert_many(docs)

def __delete_one__(coll: collection.Collection, filter: dict):
   return coll.delete_one(filter)

def __delete_many__(coll: collection.Collection, filter: dict):
   return coll.delete_many(filter)

def __find_one_and_replace__(coll: collection.Collection, filter: dict, new_doc: dict):
   return coll.find_one_and_replace(filter, new_doc)

def __find_one_and_delete__(coll: collection.Collection, filter: dict):
   return coll.find_one_and_delete(filter)

def __find_one__(coll: collection.Collection, filter: dict, projection):
   return coll.find_one(filter=filter, projection=projection)

def __find_many__(coll: collection.Collection, filter: dict, projection, **kwargs):
   return coll.find(filter=filter, projection=projection, **kwargs)
