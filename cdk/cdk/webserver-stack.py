# Stack deploys pre-requisite Alexa Skill resources

from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_ec2 as ec2,
)
from constructs import Construct
# from .cdk_stack import CdkStack

class AlexaSkillCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
    
        # Create object which references the CdkStack import
        # alexa_skill_infra = CdkStack(
        #     self, "AlexaSkillBucket",
        # )
      
    # Amazon Linux 2
    ec2.Instance(self, "AskAmeliaFrontServer",
        vpc=vpc,
        instance_type=instance_type,
        machine_image=ec2.AmazonLinuxImage()
    )