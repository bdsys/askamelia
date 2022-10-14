from constructs import Construct
from aws_cdk import (
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,

)

from cdk.pipeline_stage import PipelineStage
# from cdk.pipeline_stage import PipelineStage, PipelineStageWebInfra

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
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ],
                primary_output_directory='cdk/cdk.out',
            ),
        )
        
        deploy_base_infra = PipelineStage(self, "Deploy")
        # deploy_web_infra = PipelineStageWebInfra(self, "deploy-web-infra")
        deploy_stage = pipeline.add_stage(deploy_base_infra)
        # deploy_stage_web_infra = pipeline.add_stage(deploy_web_infra)
