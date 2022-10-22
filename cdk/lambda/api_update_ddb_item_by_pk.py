# TODO --
## Needs input validations!

import json, boto3, os

ddb_resource = boto3.resource('dynamodb')  

def lambda_handler(event, context):
    
    print (f"event: {event}")
    print (f"context {context}")

    print("Calling function update_table_item_by_pk")
    
    # Function takes a single key and value to perform an upate
    
    # Test case -- DISABLE ME ONCE THE FULL IMPLEMENTATION IS TESTED
    update_table_return = update_table_item_by_pk(
        os.environ['ask_amelia_property_ddb_table'],
        os.environ["ask_amelia_primary_key_static"],
        "test_value",
        "69"
    )

    # TODO -- THIS IS THE ACTUAL IMPLEMENTATION THAT NEEDS TO BE TESTED
    # Body will be a JSON payload with keys representing properties of the item to be updated
    # for key in event[keys]:
    #     update_table_item_by_pk(
    #         os.environ['ask_amelia_property_ddb_table'],
    #         os.environ["ask_amelia_primary_key_static"],
    #         key,
    #         key[value]
    #     )

    print(f"Update function return: {update_table_return}")

    formatted_return = dict()
    
    formatted_return["status"] = "success"
    formatted_return["operation_message"] = update_table_return
    
    http_status_code_return = 200
    http_body_return = json.dumps(formatted_return)
        
    return {
        'statusCode': http_status_code_return,
        'body': http_body_return
    }


def update_table_item_by_pk(table, pk_value, update_key, update_value):
    
    print("Invoked function update_table_item_by_pk")
    print("Passed args:")
    print(f"table:{table}")
    print(f"pk_value:{pk_value}")
    print(f"update_key: {update_key}")
    print(f"update_value: {update_value}")
    
    table = ddb_resource.Table(table)
    
    update_response = table.update_item(
        Key={
            'subject': os.environ["ask_amelia_primary_key_static"],
        },
        UpdateExpression=f"set {update_key} = :u_k",
        ExpressionAttributeValues={
            ':u_k': update_value
        },
        ReturnValues="UPDATED_NEW"
    )
    
    
    print (f"response return will be: {update_response}")
    
    return update_response
