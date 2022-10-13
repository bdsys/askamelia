# Stack deploys pre-requisite Alexa Skill resources

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    # aws_lambda_event_sources as lambda_trigger, # Alexa isn't supported yet
    # as an event source.
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_iam as iam,
    RemovalPolicy,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Defines an AWS Lambda resource
        _lambda.Function(
            self, 'AskAmeliaHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.lambda_handler', # <cdk_folder>/lambda/handler.py
            environment={
                'RESERVED_KEY': "RESERVED_VALUE",
            }
        )
        
        # Define IAM Roles
        # Lambda execution role
        ### TBD
        
        # Alexa Role
        alexa_appkit_role = iam.Role(
            self, "AskAmeliaS3AlexaRole",
            assumed_by=iam.ServicePrincipal("alexa-appkit.amazon.com"),
            description="IAM Role for Alexa appkit to access S3.",
        )
        
        # Define S3 bucket
        
        skill_bucket = s3.Bucket(
            self, "AskAmeliaSkillAssetsBucket",
            encryption = s3.BucketEncryption.S3_MANAGED,
            )
        
        
        # ddb.Table(
        #     self, 'AskAmeliaDynamoTableProperties',
        #     partition_key={'name': 'property', 'type': ddb.AttributeType.STRING},
        #     removal_policy=RemovalPolicy.DESTROY # Dynamo tables aren't
        #     # # destroyed with a stack is deleted. This property will override
        #     # # CFN default and produce a destructive action.
        # )
        
        # Permissions
        skill_bucket.grant_read(alexa_appkit_role)