import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')

def handler():
    table = dynamodb.Table('iimdb-dev')
    insert_item(table=table)

def insert_item(table):
   obj = {
      'id': str(uuid.uuid4())
   }
   
   response = table.put_item(Item=obj)
   print(response)
   

if __name__ == "__main__":
  handler()
