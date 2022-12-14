from constructs import Construct
from aws_cdk import (
    Stage
)
from .cdk_stack import CdkStack
from .webserver_stack import AlexaWebInfraCdkStack

class PipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkStack(self, 'AskAmeliaAlexaAppInfra')

class PipelineStageWebInfra(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        web_infra = AlexaWebInfraCdkStack(self, 'AskAmeliaWebInfra') 