# Stack deploys pre-requisite Alexa Skill resources

from aws_cdk import (
    Stack,
    alexa_ask as alexa,
    aws_ssm as ssm,
    aws_secretsmanager as secretsmanager,

)
from constructs import Construct
from .cdk_stack import CdkStack

class AlexaSkillCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
    
        # Create object which references the CdkStack import
        alexa_skill_infra = CdkStack(
            self, "AlexaSkillBucket",
        )
        
    
        clientSecret = secretsmanager.Secret.from_secret_attributes(self, "ImportedSecretClientSecret",
          secret_complete_arn = alexa_skill_infra.clientSecretSm.secret_arn
        )
        
        refreshToken = secretsmanager.Secret.from_secret_attributes(self, "ImportedSecretRefreshToken",
          secret_complete_arn = alexa_skill_infra.refreshTokenSm.secret_arn
        )
      
        alexa.CfnSkill(
            self, "AskAmeliaAlexaSkillFromS3",
            
            vendor_id = ssm.StringParameter.value_for_string_parameter(
                self, "vendor_id"
            ),
            
            authentication_configuration=alexa.CfnSkill.AuthenticationConfigurationProperty(
                client_id = ssm.StringParameter.value_for_string_parameter(
                    self, "client_id"
                ),
                client_secret=clientSecret,
                refresh_token=refreshToken,
            ),
            
            skill_package=alexa.CfnSkill.SkillPackageProperty(
                s3_bucket=alexa_skill_infra.skillBucket,
                s3_key="/skill-package.zip",
        
                # overrides=alexa.CfnSkill.OverridesProperty(
                #     manifest="Manifest: {apis: {custom: {endpoint: {uri:arn:aws:lambda:us-west-2:130012316542:function:Deploy-AskAmeliaAlexaAppI-AskAmeliaHandler55519923-H5gsjbrpyMdA}}}}"
                
                # ),
                
                s3_bucket_role=alexa_skill_infra.skillBucketAccessRole
            ),
        )
