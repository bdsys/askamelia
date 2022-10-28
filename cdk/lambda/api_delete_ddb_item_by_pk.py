# TODO --
## Needs input validations!

import json, boto3, os, traceback
from boto3.dynamodb.conditions import Key, Attr

ddb_client = boto3.client('dynamodb')
ddb_resource = boto3.resource('dynamodb')  

def lambda_handler(event, context):
    try:
        print (f"event: {event}")
        print (f"context {context}")
        
        try:
        
            print(f"Event PK: {event['body']}")
            
            pk_arg = json.loads(event['body'])
            pk_arg_object = pk_arg['pk']
            # pk_arg_object = "test_subject"
        
        except Exception as err:
            stackTrace = traceback.format_exc()
            print(err)
            print(stackTrace)
            http_status_code_return = 400
            http_body_return = json.dumps("Bad request")
            
            return {
                'statusCode': http_status_code_return,
                'body': http_body_return
            }
        
        print("Calling function delete_table_item_by_pk")
        
        get_items_response = delete_table_item_by_pk(
            os.environ['ask_amelia_property_ddb_table'],
            os.environ["ask_amelia_primary_key_static"],
            pk_arg_object,
        )
        
        print(f"Response sent back from delete_table_item_by_pk: {get_items_response}")
        
        formatted_return = dict()
        formatted_return["status"] = "success"
        
        http_status_code_return = 200
        http_body_return = json.dumps(formatted_return)
        
    except Exception as err_general:
        stackTrace = traceback.format_exc()
        print(err_general)
        print(stackTrace)
        print(Exception)
        http_status_code_return = 500
        http_body_return = json.dumps("Unknown error has occured!")

    return {
        'statusCode': http_status_code_return,
        'body': http_body_return
    }


def delete_table_item_by_pk(table, pk_1, pk_value):
    
    print("Invoked function delete_table_item_by_pk")
    print("Passed args:")
    print(f"table:{table}")
    print(f"pk_value:{pk_value}")

    ddb_table = ddb_resource.Table(table)
    query_response = ddb_table.delete_item(
        TableName=table,
        Key={
            pk_1: pk_value
        }
    )
    
    print (f"response return will be: {query_response}")
    
    return query_response
