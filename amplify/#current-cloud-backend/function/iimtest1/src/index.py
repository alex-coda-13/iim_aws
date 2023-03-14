import json
import os
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
  table_name = os.environ['STORAGE_IIMDB2_NAME']
  table = dynamodb.Table(table_name)

  # response = insert_elm(table=table)
  # response = get_elms_3(table=table)
  # response = update(table=table)
  # response = remove(table=table)
  response = get_batch_item(table=table, ressource=dynamodb)
  print(response)

  return {
    'body': ''
  }

# INSERT ELEMENTS

def insert_elm (table):
  obj = {
    'id1': str(uuid.uuid4()),
    'id2': 'some_sk',
    'name': 'some_name',
    'number_int': 10,
    'list_elm': ['elm_1', 'elm_2'],
    'set_elm': {
      'key_1': 'elm_1_set',
      'key_2': 'elm_2_set'
    }
  }

  response = table.put_item(Item=obj)

  return response

# GET ELEMENTS

def get_elm (table):
  try:

    # columns = {
    #   '#name': 'name'
    # }

    response = table.get_item(
      Key={
        'id1':'764586fe-3b53-4c47-8a34-1e667ff4d7f5',
        'id2': 'some_sk'
      },
      ProjectionExpression='list_elm[0], set_elm.key_1'
      # ExpressionAttributeNames=columns
    )
    
    return response['Item']

  except KeyError:
    response = 'Item not found'

  return response

def get_elm_2 (table):

  columns = {
    '#name': 'name'
  }

  # response = table.query(
  #   KeyConditionExpression=Key('id1').eq('287edf28-114b-4f46-a0e4-3a43c349e12f') & Key('id2').begins_with('som'),
  #   ProjectionExpression='id1, #name, number_int',
  #   ExpressionAttributeNames=columns,
  #   FilterExpression=Attr('number_int').eq(10)
  # )

  response = table.query(
    KeyConditionExpression=Key('id1').eq('287edf28-114b-4f46-a0e4-3a43c349e12f'),
    ProjectionExpression='id1, #name, number_int',
    ExpressionAttributeNames=columns,
    FilterExpression=Attr('number_int').eq(10)
  )

  return response['Items']

def get_elms_3 (table):
  data = []
  # response = table.scan(
  #   # ProjectionExpression='id1',
  #   # FilterExpression=Attr('list_elm[0]').eq('elm_1')
  # )
  # data.extend(response['Items'])

  # while 'LastEvaluatedKey' in response:
  #   response = table.scan(
  #     ExclusiveStartKey=response['LastEvaluatedKey']
  #   )
  #   data.extend(response['Items'])
  
  response = {}
  while True:
    kwargs = {}
    last = response.get('LastEvaluatedKey')

    if response.get('LastEvaluatedKey'):
      kwargs['ExclusiveStartKey'] = last

    response = table.scan(**kwargs)

    data.extend(response['Items'])

    if 'LastEvaluatedKey' not in response:
      break

  return data

def get_batch_item (table, ressource):

  id_list = [
    {
      'id1':'287edf28-114b-4f46-a0e4-3a43c349e12f',
      'id2': 'some_sk'
    }
  ]

  batch_keys = {
    table.name: {
      'Keys': id_list
    }
  }

  response = dynamodb.batch_get_item(
    RequestItems=batch_keys
  )

  return response['Responses'][table.name]




from math import ceil

def get_items_from_list (items_list, items_table, resource, expression = None):
  data = []
  nb_iterations = int(ceil(len(items_list) / 100))





  for iteration in range(nb_iterations):
    index_first = (iteration + 1) * 100 - 100





    index_last = (iteration + 1) * 100
    items_iteration = items_list[index_first : index_last]





    object_to_get = {
      'Keys': [{ 'id1': elm['id'] } for elm in items_iteration],
    }




    if expression is not None:
      object_to_get['ProjectionExpression'] = expression



    items_data = resource.batch_get_item(
      RequestItems={
        items_table.name: object_to_get
      }
    )



    data.extend(items_data['Responses'][items_table.name])


    while items_table.name in items_data['UnprocessedKeys']:


      object_to_get['Keys'] = items_data['UnprocessedKeys'][items_table.name]['Keys'],
      items_data = resource.batch_get_item(
        RequestItems={
          items_table.name: object_to_get
        }
      )
      data.extend(items_data['Responses'][items_table.name])

  return data

# UPDATE

def update (table):
  columns = {
    '#name': 'name'
  }

  # expression = 'SET #name = :name, number_int = number_int + :number, set_elm.key_1 = :new_elm'

  expression = 'SET list_elm = list_append(list_elm, :li)'

  # ADD number_int :number'
  # values = {
  #   ':name': 'new_name',
  #   ':number': 3,
  #   ':new_elm': 'new_elm'
  # }

  values = {
    ':li': ['elm3', 'elm4']
  }

  response = table.update_item(
    Key={
      'id1':'764586fe-3b53-4c47-8a34-1e667ff4d7f5',
      'id2': 'some_sk'
    },
    UpdateExpression=expression,
    ExpressionAttributeValues=values,
    # ExpressionAttributeNames=columns,
  )

  return response

# REMOVE

def remove (table):
  response = table.delete_item(
    Key={
      'id1':'764586fe-3b53-4c47-8a34-1e667ff4d7f5',
      'id2': 'some_sk'
    }
  )

  return response



"""
- Lambda => insert 200 éléments,
- id, sk, column_name => col_1, col_2 .... col_200
- get batch items


200 => 10 element id qui est id, sk => le même
"""