from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
)

# Tells CDK to use <cdk_base>/cdk_workshop/hitcounter.py in addition to the
# # default <cdk_base>/cdk_workshop/cdk_workshop_stack.py
from .hitcounter import HitCounter

# Third party python package "cdk-dynamo-table-view==0.2.0"
from cdk_dynamo_table_view import TableViewer


class CdkWorkshopStack(Stack):
    
    # Properties used to self-reference stack resources for CFN app stack
    # # outputs.
    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Defines an AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'HelloHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='hello.handler', # <cdk_folder>/lambda/hello.py
        )
        
        # Brings HitCounter class from .hitcounter.py in so we can access the
        # # resources in it.
        hello_with_counter = HitCounter(
            self, 'HelloHitCounter',
            downstream=my_lambda,
        )
        
        hello_gateway = apigw.LambdaRestApi(
            self, 'Endpoint',
            # handler=my_lambda,
            handler=hello_with_counter._handler,
        )

        tv_gateway = TableViewer(
            self, 'ViewHitCounter',
            title='Hello Hits',
            table = hello_with_counter.table,
        )

        # Adds CFN outputs to the CDK application stack deployed by pipeline
        # # stage.
        self._hc_endpoint = CfnOutput(
            self, 'GatewayUrl',
            value=hello_gateway.url
        )

        self._hc_viewer_url = CfnOutput(
            self, 'TableViewerUrl',
            value=tv_gateway.endpoint
        )