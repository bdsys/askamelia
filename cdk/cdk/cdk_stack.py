from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    # aws_lambda_event_sources as lambda_trigger, # Alexa isn't supported yet
    # as an event source.
    aws_dynamodb as ddb,
    RemovalPolicy,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        _lambda.Function(
            self, 'AskAmeliaHndler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.handler', # <cdk_folder>/lambda/handler.py
            environment={
                'RESERVED_KEY': "RESERVED_VALUE",
            }
        )
        
        ddb.Table(
            self, 'AskAmeliaDynamoTableProperties',
            partition_key={'name': 'property', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY # Dynamo tables aren't
            # # destroyed with a stack is deleted. This property will override
            # # CFN default and produce a destructive action.
        )