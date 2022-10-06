from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
)

class HitCounter(Construct):

    # Instructs the construct to return the defined lambda function in itself
    # # to return when asked for property HitCounter.handler.
    # # This is used to reference the lambda function since it doesn't exist
    # # as a resource to reference via an ARN or other identifier.    

    @property
    def handler(self):
        return self._handler

    # Note: The HitCounter class also takes one explicit keyword parameter 
    # # downstream of type lambda.IFunction. This is where we are going to 
    # # “plug in” the Lambda function we created in the previous chapter so it 
    # # can be hit-counted.

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs):
        super().__init__(scope, id, **kwargs)

        table = ddb.Table(
            self, 'Hits',
            partition_key={'name': 'path', 'type': ddb.AttributeType.STRING}
        )

        self._handler = _lambda.Function(
            self, 'HitCountHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='hitcount.handler',
            code=_lambda.Code.from_asset('lambda'),
            environment={
                
                # Used to export the function name as an env var upon creation.
                # # This is the only way to reference it during development.
                'DOWNSTREAM_FUNCTION_NAME': downstream.function_name,
                
                # Used to export the dynamo db table name as an env var upon 
                # # creation. This is the only way to reference it during 
                # # development.
                'HITS_TABLE_NAME': table.table_name,

            }
        )

        # Creates execution role permissions for writing to the table resource.
        # # References the lambda function defined in the construct (self).
        table.grant_read_write_data(self._handler)
        
        # Allows the lambda function defined in another construct the ability
        # # to invoke the lambda function in this construct.
        downstream.grant_invoke(self._handler)

