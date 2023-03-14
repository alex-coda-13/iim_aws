import boto3
import json

secretmanager = boto3.client('secretsmanager')

def get_secret (secret_name, secret_key):
  secret_object = secretmanager.get_secret_value(SecretId=secret_name)

  secret_values = secret_object.get('SecretString', None)

  if secret_values is None:
    raise ValueError('No keys detected')
  
  secret_json = json.loads(secret_values)
  secret_key_value = secret_json.get(secret_key, None)

  if secret_key_value is None:
    raise ValueError(f'No such key: { secret_key }')

  return secret_key_value