from .storage import *
import pymongo

# find the max value in a collection
def find_max(collection_name, filter: dict, sort_key: str, db_name="tickets"):
   sort_seq = [(sort_key, pymongo.DESCENDING)]
   return find_one(collection_name, filter, db_name=db_name, sort=sort_seq)

# find the min value in a collection
def find_min(collection_name, filter: dict, sort_key: str, db_name="tickets"):
   sort_seq = [(sort_key, pymongo.ASCENDING)]
   return find_one(collection_name, filter, db_name=db_name, sort=sort_seq)

def find_many_ascending_order(collection_name, filter: dict, sort_key: str, db_name="tickets"):
   sort_seq = [(sort_key, pymongo.ASCENDING)]
   return find_many(collection_name, filter, db_name=db_name, sort=sort_seq)
