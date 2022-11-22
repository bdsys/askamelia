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
        # api_get_ddb_items_by_pk_execution_role = iam.Role(
        #     self, "APIGetDdbTableByPkExecutionRole",
        #     assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        #     description="Lambda execution role for function APIGetDdbTableByPk"
        # )
        
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
        # DynamoDB Table get item scan
        
        api_get_ddb_items = _lambda.Function(
            self, 'APIGetDdbItems',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('lambda'),
            handler = 'api_get_ddb_pks.lambda_handler', # <cdk_folder>/lambda/api_get_ddb_items_by_pk.py
            environment = {
                'RESERVED_KEY': "RESERVED_VALUE",
                "ask_amelia_property_ddb_table": ask_amelia_property_ddb_table.table_name,
            }
        )
        
        # DynamoDB Table get item with primary key
        
        api_get_ddb_items_by_pk = _lambda.Function(
            self, 'APIGetDdbItemsByPk',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('lambda'),
            # role = api_get_ddb_items_by_pk_execution_role,
            handler = 'api_get_ddb_items_by_pk.lambda_handler', # <cdk_folder>/lambda/api_get_ddb_items_by_pk.py
            environment = {
                'RESERVED_KEY': "RESERVED_VALUE",
                "ask_amelia_property_ddb_table": ask_amelia_property_ddb_table.table_name,
                "ask_amelia_primary_key_static": "subject",
                "ask_amelia_primary_key_value_static": "amelia_cat",
            }
        )
        
        # DynamoDB Table update item with primary key
        
        api_update_ddb_item_by_pk = _lambda.Function(
            self, 'APIUpdateDdbItemByPk',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('lambda'),
            handler = 'api_update_ddb_item_by_pk.lambda_handler', # <cdk_folder>/lambda/api_get_ddb_items_by_pk.py
            environment = {
                'RESERVED_KEY': "RESERVED_VALUE",
                "ask_amelia_property_ddb_table": ask_amelia_property_ddb_table.table_name,
                "ask_amelia_primary_key_static": "subject",
                "ask_amelia_primary_key_value_static": "amelia_cat",
            }
        )
        
        # DynamoDB Table delete item with primary key
        
        api_delete_ddb_item_by_pk = _lambda.Function(
            self, 'APIDeleteDdbItemByPk',
            runtime = _lambda.Runtime.PYTHON_3_9,
            code = _lambda.Code.from_asset('lambda'),
            handler = 'api_delete_ddb_item_by_pk.lambda_handler', # <cdk_folder>/lambda/api_get_ddb_items_by_pk.py
            environment = {
                'RESERVED_KEY': "RESERVED_VALUE",
                "ask_amelia_property_ddb_table": ask_amelia_property_ddb_table.table_name,
                "ask_amelia_primary_key_static": "subject",
            }
        )
        
        # Delivery
        
        # API for getting DDB table PKs
        apigww_ask_amelia_alexa_app_api_get_pks = apigateway.LambdaRestApi(
            self, 
            "AskAmeliaAlexaAppApiGetPks",
            handler = api_get_ddb_items,
        )
        
        # API for getting DDB table items by PK
        apigw_ask_amelia_alexa_app_api_get_items_by_pk = apigateway.LambdaRestApi(
            self, 
            "AskAmeliaAlexaAppApiGetItemsByPk",
            handler = api_get_ddb_items_by_pk,
        )
        
        # API for updating DDB table item by PK
        apigw_ask_amelia_alexa_app_api_update_item_by_pk = apigateway.LambdaRestApi(
            self, 
            "AskAmeliaAlexaAppApiUpdateItemByPk",
            handler = api_update_ddb_item_by_pk,
        )
        
        # API for deleting DDB table item by PK
        apigw_ask_amelia_alexa_app_api_delete_item_by_pk = apigateway.LambdaRestApi(
            self, 
            "AskAmeliaAlexaAppApiDeleteItemByPk",
            handler = api_delete_ddb_item_by_pk,
        )
        
        # Dependent Alexa resources
        # Alexa app handler
        ask_amelia_handler = _lambda.Function(
            self, 'AskAmeliaHandler',
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='alexa_ask_amelia.lambda_handler', # <cdk_folder>/lambda/alexa_ask_amelia.py
            environment={
                'RESERVED_KEY': "RESERVED_VALUE",
                # Use prod stage by default
                'AA_API_GET_DB_ITEMS_URL': f"https://{apigww_ask_amelia_alexa_app_api_get_pks.rest_api_id}.execute-api.{self.region}.amazonaws.com/prod"
            }
        )
        
        # API for accessing Ask Amelia
        # 11/22/22 -- Doesn't work because Alexa needs a response back that
        ## AWS API Gateway can't provide.
        # apigw_ask_amelia_alexa_app_api_gateway = apigateway.LambdaRestApi(
        #     self, 
        #     "AskAmeliaAlexaAppApiGateway",
        #     handler = ask_amelia_handler,
        # )
        
        # Permissions
        # Alexa service principal perms to S3 bucket for Alexa app deployment
        self.skill_bucket.grant_read(self.alexa_appkit_role)
    
        ask_amelia_property_ddb_table.grant_read_write_data(api_get_ddb_items)
        ask_amelia_property_ddb_table.grant_read_write_data(api_get_ddb_items_by_pk)
        ask_amelia_property_ddb_table.grant_read_write_data(api_update_ddb_item_by_pk)
        ask_amelia_property_ddb_table.grant_read_write_data(api_delete_ddb_item_by_pk)

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
