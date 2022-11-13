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

def handler(event, context):
    url = URL + "/tracking?shipment_number=" + \
        event['body']['Attribute']['shipment_number']
    headers = HEADER
    m_body = str(event['body'])
    response = requests.get(url, headers=headers)
    res = response.json()

    for post in res['data']:
        if post['return_status'] == 'delivered':
            SQS.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=m_body
            )