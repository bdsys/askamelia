# Stack deploys pre-requisite Alexa Skill resources

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    # aws_lambda_event_sources as lambda_trigger, # Alexa isn't supported yet
    # as an event source.
    aws_dynamodb as ddb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ssm as ssm,
    aws_secretsmanager as secretsmanager,
    RemovalPolicy,
)
from constructs import Construct

class CdkStack(Stack):
    
    @property
    def skillBucket(self):
        return self.skill_bucket
        
    @property
    def skillBucketAccessRole(self):
        return self.alexa_appkit_role
        
    @property
    def clientSecretSm(self):
        return self.client_secret_sm
        
    @property
    def refreshTokenSm(self):
        return self.refresh_token_sm
        
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
        self.alexa_appkit_role = iam.Role(
            self, "AskAmeliaS3AlexaRole",
            assumed_by=iam.ServicePrincipal("alexa-appkit.amazon.com"),
            description="IAM Role for Alexa appkit to access S3.",
        )
        
        # Define S3 bucket
        
        self.skill_bucket = s3.Bucket(
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
        
        # Parameter and secret resources needed for upstream stacks
        vendor_id_param = ssm.StringParameter(self, "VendorIdParameter",
            parameter_name = 'vendor_id',
            description = 'Alexa developer vendor Id',
            string_value ="Initial parameter value",
        )
        
        client_id_param = ssm.StringParameter(self, "ClientIdParameter",
            parameter_name = 'client_id',
            description = 'Alexa developer client Id',
            string_value ="Initial parameter value",
        )
        
        vpc_id = ssm.StringParameter(self, "RegionalVpcIdFrontWebInfra",
            parameter_name = 'vpc_id',
            description = 'VPC Id for front web server EC2 infrastructure',
            string_value ="Initial parameter value",
        )
        
        self.client_secret_sm = secretsmanager.Secret(self, "ClientSecret",
            description = "Alexa developer client secret" 
        )
        
        self.refresh_token_sm = secretsmanager.Secret(self, "RefreshToken",
            description = "Alexa developer refresh token" 
        )
        
        # Permissions
        self.skill_bucket.grant_read(self.alexa_appkit_role)