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

def addUser(event, context):
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
        'doggy': body["doggy"],
        'race': body["race"],
        'age': body["age"]
    }
    print(json.dumps(item))
    table.put_item(
       Item=item
    )
    
def getUser(pk):
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Dogs')
    
    try:
        response = table.get_item(Key={'pk': pk})
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Item']
    
    
def setUser(pk, name, doggy, race, age):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Dogs')

    response = table.update_item(
        Key={
            'pk': pk,
            'name': name,
            'doggy':doggy,
            'race': race,
            'age': age
        },
        UpdateExpression="set info.age=:a, info.name=:n, info.doggy=:d, info.race =:r",
        ExpressionAttributeValues={
            ':a': Decimal(age),
            ':n': name,
            ':d': doggy,
            ':r': race
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }