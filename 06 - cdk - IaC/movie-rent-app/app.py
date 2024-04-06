#!/usr/bin/env python3
import os

import aws_cdk as cdk
from movie_rent_app.movie_rent_app_stack import MovieRentAppStack
from movie_rent_app.users_app_stack import UsersAppStack


app = cdk.App()

MovieRentAppStack(app, "MovieRentAppStack",
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    )

UsersAppStack(app, "MovieUsersAppStack",
        env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),)

app.synth()
