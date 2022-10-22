# TODO --
## https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.update_item
## Needs input validations!

import json, boto3, os
from boto3.dynamodb.conditions import Key, Attr

ddb_client = boto3.client('dynamodb')

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps("Not yet implemented")
    }


def update_table_item_by_pk(table, pk_value):
    return None