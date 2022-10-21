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
    aws_sns as sns,
    aws_apigateway as apigateway,
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

        # Define IAM Roles
        # Lambda execution role
        api_get_ddb_table_by_pk_execution_role = iam.Role(
            self, "APIGetDdbTableByPkExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Lambda execution role for function APIGetDdbTableByPk"
        )
        
        # Alexa Role
        self.alexa_appkit_role = iam.Role(
            self, "AskAmeliaS3AlexaRole",
            assumed_by=iam.ServicePrincipal("alexa-appkit.amazon.com"),
            description="IAM Role for Alexa appkit to access S3.",
        )
        
        # Data tier
        
        # S3 bucket
        # Alexa app assets bucket
        self.skill_bucket = s3.Bucket(
            self, "AskAmeliaSkillAssetsBucket",
            encryption = s3.BucketEncryption.S3_MANAGED,
            )
        
        # DDB Table
        # Properties table
        ask_amelia_property_ddb_table = ddb.Table(
            self, 'AskAmeliaDynamoTableProperties',
            partition_key={'name': 'subject', 'type': ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY # Dynamo tables aren't
            # # destroyed with a stack is deleted. This property will override
            # # CFN default and produce a destructive action.
        )

        # App tier
        # Lambda resources
        # Alexa app handler
        _lambda.Function(
            self, 'AskAmeliaHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='handler.lambda_handler', # <cdk_folder>/lambda/handler.py
            environment={
                'RESERVED_KEY': "RESERVED_VALUE",
            }
        )
        
        # DynamoDB Table get content with primary key
        
        api_get_ddb_table_by_pk = _lambda.Function(
            self, 'APIGetDdbTableByPk',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('lambda'),
            role = api_get_ddb_table_by_pk_execution_role,
            handler = 'api_get_ddb_table_by_pk.lambda_handler', # <cdk_folder>/lambda/api_get_ddb_table_by_pk.py
            environment = {
                'RESERVED_KEY': "RESERVED_VALUE",
                "ask_amelia_property_ddb_table": ask_amelia_property_ddb_table.table_name,
            }
        )
        
        # Delivery

        ask_amelia_alexa_app_api = apigateway.LambdaRestApi(self, "AskAmeliaAlexaAppApi",
            handler = api_get_ddb_table_by_pk
        )
        
        # ask_amelia_alexa_app_api = apigateway.RestApi(self, "AskAmeliaAlexaAppApi")
        
        # ask_amelia_alexa_app_api.add_proxy(
        #     default_integration=apigateway.LambdaIntegration(api_get_ddb_table_by_pk),
        
        #     # "false" will require explicitly adding methods on the `proxy` resource
        #     any_method=True
        # )


        # Permissions
        # Alexa service principal perms to S3 bucket for Alexa app deployment
        self.skill_bucket.grant_read(self.alexa_appkit_role)
    
        ask_amelia_property_ddb_table.grant_read_write_data(api_get_ddb_table_by_pk)




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
        
        instance_type_front_web = ssm.StringParameter(self, "FrontWebInstanceType",
            parameter_name = 'instance_type_front_web',
            description = 'Family.size instance type for web front EC2 instances.',
            string_value ="Initial parameter value",
        )
        
        front_web_ami_id = ssm.StringParameter(self, "FrontWebAmiId",
            parameter_name = 'front_web_ami_id',
            description = 'AMI Id for front web EC2 instances.',
            string_value ="Initial parameter value",
        )
        
        bastion_source_cidr = ssm.StringParameter(self, "BastionSourceCidr",
            parameter_name = 'bastion_source_cidr',
            description = 'Source IPv4 CIDR for Bastion source.',
            string_value ="Initial parameter value",
        )
        
        ssh_key_name_front_web = ssm.StringParameter(self, "SshKeyNameFrontWeb",
            parameter_name = 'ssh_key_name_front_web',
            description = 'SSH Key EC2 resource for front web.',
            string_value ="Initial parameter value",
        )
        
        self.client_secret_sm = secretsmanager.Secret(self, "ClientSecret",
            description = "Alexa developer client secret" 
        )
        
        self.refresh_token_sm = secretsmanager.Secret(self, "RefreshToken",
            description = "Alexa developer refresh token" 
        )
        
        dev_email_topic = sns.Topic(
            self, "dev_email_topic"
        )
