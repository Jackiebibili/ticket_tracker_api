from utils import get_db_handle
from .base import *

# insert one
def insert_one(collection_name, doc: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   # additional attributes
   doc.update(gen_additional_attrs())
   return insert_one__(coll, doc)

# insert many
def insert_many(collection_name, docs: list[dict], db_name="tickets"):
   if len(docs) == 0:
      return True
   db = get_db_handle(db_name)
   coll = db[collection_name]
   # additional attributes
   for doc in docs:
      doc.update(gen_additional_attrs())
   return insert_many__(coll, docs)

# delete one
def delete_one(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return delete_one__(coll, filter)

# delete many
def delete_many(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return delete_many__(coll, filter)

# find one and replace
def find_one_and_replace(collection_name, filter: dict, new_doc: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return find_one_and_replace__(coll, filter, new_doc)

# find one and update
def find_one_and_update(collection_name, filter: dict, update, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return find_one_and_update__(coll, filter, update)

# find one and delete
def find_one_and_delete(collection_name, filter: dict, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return find_one_and_delete__(coll, filter)

# find one
def find_one(collection_name, filter: dict, projection=None, db_name="tickets"):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return find_one__(coll, filter, projection)

# find many
def find_many(collection_name, filter: dict, projection=None, db_name="tickets", **kwargs):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return list(find_many__(coll, filter, projection, **kwargs))

# watch changes
def watch(collection_name, db_name="tickets", **kwargs):
   db = get_db_handle(db_name)
   coll = db[collection_name]
   return watch__(coll, **kwargs)

