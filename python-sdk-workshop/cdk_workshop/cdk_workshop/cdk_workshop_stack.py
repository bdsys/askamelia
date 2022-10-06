from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

# Tells CDK to use <cdk_base>/cdk_workshop/hitcounter.py in addition to the
# # default <cdk_base>/cdk_workshop/cdk_workshop_stack.py
from .hitcounter import HitCounter

class CdkWorkshopStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler', # <cdk_folder>/lambda/hello.py
        )
        
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )
        
        apigw.LambdaRestApi(
            self, 'Endpoint',
            # handler=my_lambda,
            handler=hello_with_counter._handler,
        )
