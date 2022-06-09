from ..utils import get_db_handle
from .base import *
from uuid import uuid4

# insert one
def insert_one(collection_name, doc: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   doc["_id"] = str(uuid4())
   coll = db[collection_name]
   return __insert_one__(coll, doc)

# insert many
def insert_many(collection_name, docs: list, db_name="tickets"):
   db = get_db_handle(db_name)
   for doc in docs:
      doc["_id"] = str(uuid4())
   coll = db[collection_name]
   return __insert_many__(coll, docs)

# delete one
def delete_one(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __delete_one__(coll, filter)

# delete many
def delete_many(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __delete_many__(coll, filter)

# find one and replace
def find_one_and_replace(collection_name, filter: dict, new_doc: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __find_one_and_replace__(coll, filter, new_doc)

# find one and delete
def find_one_and_delete(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __find_one_and_delete__(coll, filter)

# find one
def find_one(collection_name, filter: dict, projection=None, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __find_one__(coll, filter, projection)

# find many
def find_many(collection_name, filter: dict, projection=None, db_name="tickets", **kwargs):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return __find_many__(coll, filter, projection, **kwargs)