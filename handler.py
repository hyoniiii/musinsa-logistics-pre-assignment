import json
import logging
import os
import requests

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv('QUEUE_URL')
SQS = boto3.client('sqs')
URL = "https://moms.dev.musinsalogistics.co.kr/api/external/data"
TOKEN = {
    'Authorization': 'Bearer b8040a33ea0cc60aeb9df93240d429198bbe6f034c4e0fe444b08fe0542659bd'
}

def returns(event, context):
    status_code = 200;
    message = ''

    url = URL + "/returns"
    headers = TOKEN
    response = requests.get(url, headers)
    
    try:
        for params in response['data']:
            message_attrs = {
                'Attribute': {
                    'id': params['id'],
                    'order_number': params['order_number'],
                    'order_item_number': params['order_item_number'],
                    'shipment_number': params['shipment_number']
                }
            }
            SQS.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=event['body'],
                MessageAttributes=message_attrs,
            )
        message = 'Message accepted!'
    except Exception as e:
        logger.exception('Sending message to SQS queue failed!')
        message = str(e)
        status_code = 500

    return {'statusCode': status_code, 'body': json.dumps({'message': message})}


def delivers(event, context):
    url = URL + "/tracking?shipment_number=" + event['body']['Attribute']['shipment_number']
    headers = TOKEN
    m_body = str(event['body'])
    response = requests.get(url, headers=headers)
    res = response.json()

    for post in res['data']:
        if post['return_status'] == 'delivered':
            SQS.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=m_body
            )

def results(event, context):
    url = URL + "/results"
    headers = TOKEN
    data = {
        'order_number': event['body']['Attribute']['order_number'],
        'order_item_number': event['body']['Attribute']['order_item_number'],
        'result_object': 'delivered'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.data.result != True:
        SQS.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=event['body'],
            MessageAttributes=event['body']['Attribute']
        )