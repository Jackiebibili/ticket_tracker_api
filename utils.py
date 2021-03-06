from pymongo import MongoClient
from secret import CONN_SRV

client = MongoClient(CONN_SRV)

def get_db_handle(db_name):
    global client
    db_handle = client[db_name]
    return db_handle
