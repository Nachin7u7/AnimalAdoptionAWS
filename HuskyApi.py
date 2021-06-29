from pprint import pprint
from decimal import Decimal
import json
import boto3
import os
from botocore.exceptions import ClientError
 ## Huscky Shelter API
accounts_table = os.environ['ACCOUNTS-TABLE']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(accounts_table)

def putPet(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    account_id = path.split("/")[-1] # ["account", "id"]
    
    body = json.loads(event["body"])
    print(body)
    print(account_id)
    item = {
        'pk': account_id,
        'name': body["name"],
        'race': body["race"],
        'age': body["age"]
    }
    print(json.dumps(item))
    table.put_item(
       Item=item
    )
    
    print(json.dumps(item))
    table.put_item(
       Item=item
    )
    
    
def getPet(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    pet_id = path.split("/")[-1] # ["user", "id"]
    
    response = table.get_item(
        Key={
            'pk': pet_id,
            'sk': 'profile'
        }
    )
    item = response['Item']
    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }