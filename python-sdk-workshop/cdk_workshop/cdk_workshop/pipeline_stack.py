from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,

)

from cdk_workshop.pipeline_stage import WorkshopPipelineStage

class WorkshopPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'WorkshopRepo'
        repo = codecommit.Repository(
            self, 'WorkshopRepo',
            repository_name= "WorkshopRepo"
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "cd python-sdk-workshop/cdk_workshop/", # move to CDK base
                    "ls", # list dir to show whats up
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ],
                primary_output_directory='python-sdk-workshop/cdk_workshop/cdk.out',
                # primary_output_directory='cdk_workshop/cdk.out',
            ),
        )
        
        deploy = WorkshopPipelineStage(self, "Deploy")
        deploy_stage = pipeline.add_stage(deploy)

