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


        # vpc_id = ssm.StringParameter.value_for_string_parameter(
        #     self, "vpc_id"
        # ),

        vpc_id = ssm.StringParameter.value_from_lookup(
            self, "vpc_id"
        ),
        
        front_web_instance_type = ssm.StringParameter.value_from_lookup(
            self, "instance_type_front_web"
        ),
        
        front_web_ami_id = ssm.StringParameter.value_from_lookup(
            self, "web_front_ami_id"
        ),
        
        bastion_source_cidr = ssm.StringParameter.value_from_lookup(
            self, "bastion_source_cidr"
        ),
    
        ssh_key_name_front_web = ssm.StringParameter.value_from_lookup(
            self, "ssh_key_name_front_web"
        ),
    
        # Objects
        front_web_ami = ec2.GenericLinuxImage({ 
            "us-west-2": front_web_ami_id[0]
            # "us-west-2":"ami-08970fb2e5767e3b8"
        })
          
        # Security groups
        
        front_web_server_sg = ec2.SecurityGroup(
            self, "FrontWebServerSg",
                vpc = vpc_id[0],
                description = "SG 1 for front web servers.",
                allow_all_outbound = True,
        )
        
        # Security group ingress rules
        front_web_server_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(bastion_source_cidr[0]),
            connection=ec2.Port.tcp(22),
            description="SSH from Bastion",
        )
        
        front_web_server_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(bastion_source_cidr[0]),
            connection=ec2.Port.tcp(443),
            description="HTTPS from Bastion",
        )
        
        front_web_server_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(bastion_source_cidr[0]),
            connection=ec2.Port.tcp(80),
            description="HTTP from Bastion",
        )
        
        front_web_server_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(bastion_source_cidr[0]),
            connection=ec2.Port.tcp(5000),
            description="HTTP on tcp/5000 from Bastion",
        )
        
        # Amazon Linux 2
        ec2.Instance(self, "AskAmeliaFrontServer",
            vpc = vpc_id[0],
            instance_type = ec2.InstanceType(front_web_instance_type[0]),
            machine_image=front_web_ami[0],
            key_name = ssh_key_name_front_web[0],
            # role = x,# TODO
            security_group = front_web_server_sg[0],
        )
