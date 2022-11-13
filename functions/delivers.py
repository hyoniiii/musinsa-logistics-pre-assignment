import json
import logging
import os
import requests

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

QUEUE_URL = os.getenv('QUEUE_URL')
TOKEN = os.getenv('TOKEN')
BASE_URL = os.getenv('BASE_URL')
SLACK_URL = os.getenv('SLACK_URL')
SQS = boto3.client('sqs')
HEADER = {
    'Authorization': 'Bearer ' + TOKEN
}


def slack_message(error):
    url = SLACK_URL
    data = {
        "text": error
    }
    response = requests.post(url, json=data)
    return response


def send_msg(event, context):
    url = BASE_URL + "/tracking?shipment_number=" + \
        event['body']['Attribute']['shipment_number']
    headers = HEADER
    response = requests.get(url, headers=headers)
    return response.json()


def handler(event, context):
    m_body = str(event['body'])

    res = send_msg(event, context)

    for post in res['data']:
        if post['return_status'] == 'delivered':
            SQS.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=m_body
            )

    # if res['data'] == []:
    slack_message('No return found for shipment number ' +
                  event['body']['Attribute']['shipment_number'])
