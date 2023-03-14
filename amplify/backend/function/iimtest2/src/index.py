import json
import boto3
import os
from botocore.exceptions import ClientError
import uuid
from boto3.dynamodb.conditions import Attr

from utils import get_secret

dynamodb = boto3.resource('dynamodb')

MAX_SIZE = 200

def handler(event, context):
  response  = {}
  try:

    headers = event.get('headers') or {}
    api_key = headers.get('x-api-key')

    if not api_key:
      raise ValueError('Input error: x-api-key')
    
    client_name = get_secret('iim_api', api_key)
    print(client_name)

    table_name = os.environ['STORAGE_IIMDB2_NAME']
    table = dynamodb.Table(table_name)

    # insert_elements(table)

    filter_expression = Attr('id2').eq('some_sk_5') | Attr('id2').eq('some_sk_6')
    projection = 'id1, id2, some_column'
    data = scan(table, filter_expression, projection)

    # for elm in data:
    #   key = {
    #     'id1': elm['id1'],
    #     'id2': elm['id2']
    #   }

      # list_elm = [1, 2, 3]

      # expression = 'SET list_elm = list_append( if_not_exists(list_elm, :empty), :list_elm)'
      # values = {
      #   ':list_elm': list_elm,
      #   ':empty': []
      # }

      # expression = 'REMOVE list_elm[1]'

      # update(table, key, expression)

    response['statusCode'] = 200
    response['body'] = json.dumps(data)
  except (Exception, ClientError) as error:
    response['statusCode'] = 400
    response['body'] = json.dumps({ 'error': str(error) })

  return response

def insert_elements (table):
  nb_elm = 0
  sk_batch = 0

  while nb_elm < MAX_SIZE:

    table.put_item(Item={
      'id1': str(uuid.uuid4()),
      'id2': 'some_sk_' + str(sk_batch),
      'some_column': 'col_' + str(nb_elm)
    })

    if nb_elm % 10 == 0:
      sk_batch += 1

    nb_elm += 1

def scan (table, filter_expression, projection):
  data = []
  response = {}
  while True:
    kwargs = {
      'FilterExpression': filter_expression,
      'ProjectionExpression': projection
    }

    last = response.get('LastEvaluatedKey')

    if response.get('LastEvaluatedKey'):
      kwargs['ExclusiveStartKey'] = last

    response = table.scan(**kwargs)

    data.extend(response['Items'])

    if 'LastEvaluatedKey' not in response:
      break

  return data


def update (table, key, expression, values = None):
  table.update_item(
    Key=key,
    UpdateExpression=expression
    # ExpressionAttributeValues=values
  )
