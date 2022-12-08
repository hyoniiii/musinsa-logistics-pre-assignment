import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugin import request, mongo

def app_handler():
  raw_data = request.get_return()
  data_list = raw_data['data']
  # print(data_list)
  for i in data_list:
    mongo.insert_data(i)
    
