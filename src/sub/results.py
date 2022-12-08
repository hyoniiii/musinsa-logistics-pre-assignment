import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugin import request, mongo

def app_handler():
  data_list = []
  
  for i in mongo.fetch_data(20):
    data_list.append(i)

  for i in range(len(data_list)):
    for j in range(i+1, len(data_list)):
      if data_list[i]['shipment_number'] == data_list[j]['shipment_number']:
        del data_list[j]
        break 
    
  for data in data_list:
    return_status = data['return_status']
    if return_status == 'delivered':
      req_data = {
        "order_number": data['order_number'],
        "order_item_number": data['order_item_number'],
        "result_object": True
      }
      res = request.post_result(req_data)
      # print(res)
      mongo.delete_data(data)
      
# app_handler()