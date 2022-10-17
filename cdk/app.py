#!/usr/bin/env python3
import aws_cdk as cdk
from cdk.pipeline_stack import PipelineStack

app = cdk.App()

env_dev = cdk.Environment(account="130012316542", region="us-west-2")

# Main construct file
PipelineStack(app, "PipelineStack", env=env_dev)

# CFN synthesis signals the end of the CDK app
app.synth()
