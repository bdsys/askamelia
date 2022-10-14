# Stack deploys pre-requisite Alexa Skill resources

from aws_cdk import (
    Stack,
    aws_ssm as ssm,
    aws_ec2 as ec2,
)
from constructs import Construct
# from .cdk_stack import CdkStack

class AlexaWebInfraCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        vpc_id = ssm.StringParameter.value_for_string_parameter(
            self, "vpc_id"
        ),
        
        front_web_instance_type = ssm.StringParameter.value_for_string_parameter(
            self, "instance_type_front_web"
        ),
        
        front_web_ami_id = ssm.StringParameter.value_for_string_parameter(
            self, "web_front_ami_id"
        ),
        
        front_web_ami = ec2.GenericLinuxImage({
            "us-west-2": front_web_ami_id
        })
          
        # Amazon Linux 2
        ec2.Instance(self, "AskAmeliaFrontServer",
            vpc = vpc_id,
            instance_type = ec2.InstanceType(front_web_instance_type),
            machine_image=front_web_ami
        )
