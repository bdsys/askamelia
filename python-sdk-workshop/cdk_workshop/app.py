#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack


app = cdk.App()

# Construct files
CdkWorkshopStack(app, "cdk-workshop")

# CFN synthesis signals the end of the CDK app
app.synth()
