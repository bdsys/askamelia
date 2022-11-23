from constructs import Construct
import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,

)

# from cdk.pipeline_stage import PipelineStage
from cdk.pipeline_stage import PipelineStage, PipelineStageWebInfra

class PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'AskAmeliaRepo'
        repo = codecommit.Repository(
            self, 'AskAmeliaRepo',
            repository_name= "AskAmeliaRepo"
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "cd cdk/", # move to CDK base
                    "ls", # list dir to show whats up
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "cdk --version", # Check on version of CDK for potential troubleshooting
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "systemctl start docker", # Starts docker in order to pull and customize AL2 Python 3.9 image
                    "cdk synth", # Builds CDK app subject
                ],
                primary_output_directory='cdk/cdk.out',
            ),
        )
        
        # pipeline.add_stage(MyPipelineAppStage(self, "test",
        #     env=cdk.Environment(account="111111111111", region="eu-west-1")))
        
        # Define environment info
        env_dev = cdk.Environment(account="130012316542", region="us-west-2")
        
        deploy_base_infra = PipelineStage(self, "Deploy", env=env_dev)
        # deploy_web_infra = PipelineStageWebInfra(self, "deploy-web-infra", env=env_dev)
        deploy_stage = pipeline.add_stage(deploy_base_infra)
        # deploy_stage_web_infra = pipeline.add_stage(deploy_web_infra)
