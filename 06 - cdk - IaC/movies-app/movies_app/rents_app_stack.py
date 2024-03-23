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

class RentsAppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC por default para ser utilizada por todos los servicios
        vpc = aws_ec2.Vpc.from_lookup(self, "VPC",
            is_default=True
        )
        
      