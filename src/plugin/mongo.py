from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL")
DATABASE=os.getenv("DATABASE")
COLLECTION=os.getenv("COLLECTION")

client = MongoClient(MONGO_URL)

# connect to the database
db = client[DATABASE]

collection = db[COLLECTION]


def insert_data(data):
  return collection.insert_one(data)

def update_data(data):
  query = { '_id': data['_id'] }
  set_data = { '$set': { 'return_status': data['return_status']} }
  return collection.update_one(query, set_data)
  
def delete_data(data):
  query = { "shipment_number": data['shipment_number']}
  return collection.delete_many(query)
  
def fetch_data(max_data=5):
  return collection.find().limit(max_data)
