from pymongo import collection
from uuid import uuid4
from datetime import datetime

def insert_one__(coll: collection.Collection, doc: dict):
   return coll.insert_one(doc)

def insert_many__(coll: collection.Collection, docs: list):
   return coll.insert_many(docs)

def delete_one__(coll: collection.Collection, filter: dict):
   return coll.delete_one(filter)

def delete_many__(coll: collection.Collection, filter: dict):
   return coll.delete_many(filter)

def find_one_and_replace__(coll: collection.Collection, filter: dict, new_doc: dict):
   return coll.find_one_and_replace(filter, new_doc)

def find_one_and_delete__(coll: collection.Collection, filter: dict):
   return coll.find_one_and_delete(filter)

def find_one__(coll: collection.Collection, filter: dict, projection):
   return coll.find_one(filter=filter, projection=projection)

def find_many__(coll: collection.Collection, filter: dict, projection, **kwargs):
   return coll.find(filter=filter, projection=projection, **kwargs)

def gen_additional_attrs():
   return {
       "_id": str(uuid4()),
       "last_modified": datetime.today().replace(microsecond=0)
   }