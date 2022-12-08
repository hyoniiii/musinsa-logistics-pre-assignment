import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugin import request, mongo

def app_handler():
  # 데이터 불러오기
  for data in mongo.fetch_data(20):
    # 불러온 data에서 shipment_number 기준으로 현재 배송상태 확인하기
    shipment_number = data['shipment_number']
    res = request.get_delivery(shipment_number) 

    if data['return_status'] != res['data'][0]['return_status']:
      # 변경된 return_status 상태를 바탕으로 기존 데이터 변경하기 
      data['return_status'] = res['data'][0]['return_status']
      mongo.update_data(data)

# app_handler()