from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    # aws_sqs as sqs,
)
from constructs import Construct

class MovieRentAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Tabla de DynamoDB para películas
        movies_table = dynamodb.Table(self, "MoviesTable",  
            partition_key=dynamodb.Attribute(name="movie_id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,   
            removal_policy=RemovalPolicy.DESTROY,
            table_name="MovieRentApp-Movies"
        )
        
        sk_created_at = dynamodb.Attribute(name="created_at", type=dynamodb.AttributeType.STRING)
        
        movies_table.add_global_secondary_index(
            index_name="GSI_Genre",
            partition_key=dynamodb.Attribute(name="genre", type=dynamodb.AttributeType.STRING),
            sort_key=sk_created_at,
        )
        
        movies_table.add_global_secondary_index(
            index_name="GSI_Year",
            partition_key=dynamodb.Attribute(name="year", type=dynamodb.AttributeType.NUMBER),
            sort_key=sk_created_at,
        )
        
        # Bucket para posters de películas
        poster_bucket = s3.Bucket(self, "MoviePostersBucket", 
                                  removal_policy=RemovalPolicy.DESTROY,
                                  bucket_name="movierentapp-postersbucket-202404060926"
                                  )
        
        # Capa de Lambda para biblioteca de requests
        requests_layer = _lambda.LayerVersion(self, "RequestsLayer",
                                             code=_lambda.Code.from_asset("layers/requests_layer"),
                                             compatible_runtimes=[_lambda.Runtime.PYTHON_3_9]
                                             )
        
        
        # Función lambda para operaciones con películas
        movies_lambda = _lambda.Function(self, "MoviesLambda",
                                        runtime=_lambda.Runtime.PYTHON_3_9,
                                        handler="movies_lambda.handler",
                                        code=_lambda.Code.from_asset("lambda/movies"),
                                        layers=[requests_layer],
                                        timeout=Duration.seconds(10),
                                        environment={
                                            "MOVIES_TABLE": movies_table.table_name,
                                            "POSTER_BUCKET": poster_bucket.bucket_name
                                        })
        
        movies_table.grant_read_write_data(movies_lambda)
        poster_bucket.grant_read_write(movies_lambda)
        
        # API Gateway para la función
        api = apigateway.RestApi(self, "MoviesApi", 
                                rest_api_name="Movies Service",
                                description="This service serves movies."
                                )    
        
        usage_plan = api.add_usage_plan("MoviesUsagePlan", 
                          name="MoviesUsagePlan",
                          api_stages=[{"api": api, "stage": api.deployment_stage}]
                          )
        
        key = api.add_api_key("MovieServicesApiKey")
        
        usage_plan.add_api_key(key)
        
        movies_lambda_integration = apigateway.LambdaIntegration(movies_lambda)
        
        movies_resource = api.root.add_resource("movies")
        
        movies_resource.add_method("POST", movies_lambda_integration,
                                                        api_key_required=True,
                                                        authorization_type=apigateway.AuthorizationType.NONE)
        
        movies_resource.add_resource("{movie_id}").add_method("GET",
                                                              movies_lambda_integration,
                                                              api_key_required=True,
                                                              authorization_type=apigateway.AuthorizationType.NONE)
        
        