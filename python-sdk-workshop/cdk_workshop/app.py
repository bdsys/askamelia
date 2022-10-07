#!/usr/bin/env python3

import aws_cdk as cdk

# from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack
from cdk_workshop.pipeline_stack import WorkshopPipelineStack



app = cdk.App()

# Main construct file
# CdkWorkshopStack(app, "cdk-workshop")
WorkshopPipelineStack(app, "WorkshopPipelineStack")


# CFN synthesis signals the end of the CDK app
app.synth()
