#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.pipeline_stack import PipelineStack

app = cdk.App()

# Main construct file
PipelineStack(app, "PipelineStack")

# CFN synthesis signals the end of the CDK app
app.synth()
