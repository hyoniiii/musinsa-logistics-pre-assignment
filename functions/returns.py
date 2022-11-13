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
SQS = boto3.client('sqs')
HEADER = {
    'Authorization': 'Bearer ' + TOKEN
}

def handler(event, context):
    status_code = 200;
    message = ''

    url = BASE_URL + "/returns"
    headers = HEADER
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