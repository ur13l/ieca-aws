from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as aws_ec2,
    aws_lambda as aws_lambda,
    aws_rds as aws_rds,
    aws_apigateway as aws_apigateway,
    # aws_sqs as sqs,
)
from constructs import Construct

class MoviesAppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define una red VPC para alojar tu base de datos
        vpc = aws_ec2.Vpc.from_lookup(self, "VPC",
            # This imports the default VPC but you can also
            # specify a 'vpcName' or 'tags'.
            is_default=True
        )
        
       