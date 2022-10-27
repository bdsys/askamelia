# TODO --
## Needs input validations!

import json, boto3, os

ddb_resource = boto3.resource('dynamodb')  

def lambda_handler(event, context):
    
    print (f"event: {event}")
    print (f"context {context}")

    try:
    
        print(f"Event PK: {event['pk']}")
        print(f"Event pk_value: {event['pk_value']}")
        print(f"Event update_key: {event['update_key']}")
        print(f"Event update_value: {event['update_value']}")

    except Exception:
        print(Exception)
        http_status_code_return = 400
        http_body_return = json.dumps("Bad request")
        
        return {
            'statusCode': http_status_code_return,
            'body': http_body_return
        }


    print("Calling function update_table_item_by_pk")
    
    # Function takes a single key and value to perform an upate
    
    # # Test case -- DISABLE ME ONCE THE FULL IMPLEMENTATION IS TESTED
    # update_table_return = update_table_item_by_pk(
    #     os.environ['ask_amelia_property_ddb_table'],
    #     os.environ["ask_amelia_primary_key_static"],
    #     os.environ["ask_amelia_primary_key_value_static"],
    #     "test_value",
    #     "69"
    # )


    update_table_return = update_table_item_by_pk(
        os.environ['ask_amelia_property_ddb_table'],
        event['pk'],
        event['pk_value']
        event['update_key'],
        event['update_value'],
        )

    print(f"Update function return: {update_table_return}")

    formatted_return = dict()
    
    formatted_return["status"] = "success"
    formatted_return["operation_message"] = update_table_return["Attributes"]
    
    http_status_code_return = 200
    http_body_return = json.dumps(formatted_return)
        
    return {
        'statusCode': http_status_code_return,
        'body': http_body_return
    }


def update_table_item_by_pk(table, pk_1, pk_value, update_key, update_value):
    
    print("Invoked function update_table_item_by_pk")
    print("Passed args:")
    print(f"table:{table}")
    print(f"pk_1:{pk_1}")
    print(f"pk_value:{pk_value}")
    print(f"update_key: {update_key}")
    print(f"update_value: {update_value}")
    
    table = ddb_resource.Table(table)
    
    update_response = table.update_item(
        Key={
            f'{pk_1}': pk_value,
        },
        UpdateExpression=f"set {update_key} = :u_k",
        ExpressionAttributeValues={
            ':u_k': update_value
        },
        ReturnValues="ALL_NEW"
        # ALL_NEW - Returns all of the attributes of the item, as they appear after the UpdateItem operation.
        # UPDATED_NEW - Returns only the updated attributes, as they appear after the UpdateItem operation.
    )
    
    
    print (f"response return will be: {update_response}")
    
    return update_response
