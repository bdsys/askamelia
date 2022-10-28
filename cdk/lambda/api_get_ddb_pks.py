# TODO --
## Needs input validations!

import json, boto3, os, traceback
from boto3.dynamodb.conditions import Key, Attr

ddb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        print (f"event: {event}")
        print (f"context {context}")
        
        print("Calling function get_table_items")
        
        get_items_response = get_table_items(
            os.environ['ask_amelia_property_ddb_table'],
        )
        
        # print(f"Items list sent back from get_table_items: {get_items_response[0]}")
        print(f"Items list sent back from get_table_items: {get_items_response}")
        print(f"count of items in list get_items_response: {len(get_items_response)}")
        # print(get_items_response[0]["birth_date"]['S'])
        
        print("Cleaning up ddb domain specific JSON return.")
        formatted_list_return = dict()
        item_number = 0
        for item in get_items_response:
            formatted_sub_list = dict()
            sub_item_number = 0
            print(f'item {item_number}')
            print(f"item {item_number}: {item} -- {get_items_response[item_number]}")
            for sub_item in item:
                print(f'sub_item {sub_item}')
                print(f"sub_item {sub_item_number}: {sub_item} -- {get_items_response[item_number][sub_item]['S']}")
                formatted_sub_list[sub_item] = get_items_response[item_number][sub_item]['S']
                sub_item_number += 1
            formatted_list_return[item_number] = formatted_sub_list
            item_number += 1
            
        print(f"Cleaned dictonary (flat) to be returned to requester: {formatted_list_return}")
        
        print(f"Cleaned dictonary (iterated) to be returned to requester: {formatted_list_return}")
        item_number = 1
        for item in formatted_list_return:
            print(f"item {item_number}: {item} -- {formatted_list_return[item]}")
            item_number += 1
            
        http_status_code_return = 200
        http_body_return = json.dumps(formatted_list_return)
        
    except Exception as err:
        stackTrace = traceback.format_exc()
        print(err)
        print(stackTrace)
        http_status_code_return = 500
        http_body_return = json.dumps("Unknown error has occured!")

    return {
        'statusCode': http_status_code_return,
        'body': http_body_return
    }


def get_table_items(table):
    
    print("Invoked function get_table_items_by_pk")
    print("Passed args:")
    print(f"table:{table}")

    query_response = ddb_client.scan(
        TableName=table,
    )
    
    print (f"response return will be: {query_response}")
    print(f"formatted response: {query_response['Items']}")
    
    return query_response['Items']