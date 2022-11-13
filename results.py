import json
import logging
import os
import requests

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv('QUEUE_URL')
TOKEN = os.getenv('TOKEN')
URL = os.getenv('Base_URL')
SQS = boto3.client('sqs')
HEADER = {
    'Authorization': 'Bearer ' + TOKEN
}

def results(event, context):
    url = URL + "/results"
    headers = HEADER
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
