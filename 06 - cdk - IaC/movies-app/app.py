#!/usr/bin/env python3
import os

import aws_cdk as cdk

from movies_app.movies_app_stack import  MoviesAppStack
from movies_app.users_app_stack import  UsersAppStack
from movies_app.rents_app_stack import  RentsAppStack


app = cdk.App()
UsersAppStack(app, "UsersAppStack", env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
MoviesAppStack(app, "MoviesAppStack", env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))
RentsAppStack(app, "RentsAppStack", env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")))

app.synth()
