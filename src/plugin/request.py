import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_URL = os.getenv("BASE_URL")

def get_delivery(shipment_number):
  url = BASE_URL + "/tracking?shipment_number="+shipment_number
  api_key='token ' + TOKEN
  headers = {
    'Content-type': 'application/json',
    'Authorization': api_key
  }
  response = requests.get(url, headers=headers, timeout=5)
  return response.json()

def get_return():
  url = BASE_URL + "/returns"
  api_key = "token " + TOKEN
  headers = {
    'Content-type': "application/json",
    'Authorization': api_key
  }
  response = requests.get(url, headers=headers, timeout=15)
  return response.json()


def post_result(data):
  url = BASE_URL + "/results"
  api_key='token ' + TOKEN 
  headers = {
    'Content-type': 'application/json',
    'Authorization': api_key
  }
  response = requests.post(url, headers=headers, data=json.dumps(data), timeout=5)
  return response.json()
