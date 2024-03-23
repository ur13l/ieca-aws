from aws_cdk import (
    Stack,
    aws_ec2 ,
    aws_lambda as aws_lambda,
    aws_rds ,
    aws_apigateway,
    # aws_sqs as sqs,
)
from constructs import Construct

class UsersAppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define una red VPC para alojar tu base de datos
        vpc = aws_ec2.Vpc.from_lookup(self, "VPC",
            is_default=True
        )
        
        # Crear un nuevo grupo de seguridad
        security_group = aws_ec2.SecurityGroup(self, "SecurityGroupPostgres",
                                               vpc=vpc,
                                               description="Permite acceso a RDS desde una IP especifica",
                                               allow_all_outbound=True)

        # Añadir una regla de entrada para permitir el tráfico PostgreSQL desde una IP específica
        security_group.add_ingress_rule(peer=aws_ec2.Peer.ipv4('187.188.63.79/32'),
                                        connection=aws_ec2.Port.tcp(5432),
                                        description="Acceso PostgreSQL")

        # Crea una base de datos PostgreSQL en RDS utilizando configuraciones elegibles para la capa gratuita
        database = aws_rds.DatabaseInstance(self, "UserDatabase",
                                            engine=aws_rds.DatabaseInstanceEngine.postgres(version=aws_rds.PostgresEngineVersion.VER_12_3),
                                            instance_type=aws_ec2.InstanceType.of(aws_ec2.InstanceClass.BURSTABLE2, aws_ec2.InstanceSize.MICRO),
                                            vpc=vpc,
                                            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
                                            allocated_storage=20, # Configura hasta 20 GB, que es el límite para la capa gratuita
                                            max_allocated_storage=20, # Opcional, para prevenir el auto escalado
                                            deletion_protection=False, # Considera habilitar en producción
                                            credentials=aws_rds.Credentials.from_generated_secret("admin"), # Usa credenciales seguras
                                            database_name="users_db", # Nombre de tu base de datos
                                            security_groups=[security_group] # Asigna el grupo de seguridad
                                           )
        


        # Define una función Lambda para /signup
        register_authenticate_lambda = aws_lambda.Function(self, "SignupLambda",
            code=aws_lambda.Code.from_asset("lambda/users/register_authenticate"),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            environment=dict(
                DATABASE_URL=database.secret.secret_value_from_json("url").unsafe_unwrap()
            )
        )
        
         # Define una función Lambda para crear usuarios administradores
        create_admin_lambda = aws_lambda.Function(self, "CreateAdminLambda",
            code=aws_lambda.Code.from_asset("lambda/users/create_admin"),
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.handler",
            environment=dict(
                DATABASE_URL=database.secret.secret_value_from_json("url").unsafe_unwrap()
            )
        )

        # Crea un API Gateway y vincula las funciones Lambda
        api = aws_apigateway.RestApi(self, "UsersAPI")
        
        # Crear integraciones de lambda para las rutas /signup y /login pasando el método HTTP.
        register_authenticate_integration = aws_apigateway.LambdaIntegration(register_authenticate_lambda)
        
        
        api.root.resource_for_path("signup").add_method("POST", register_authenticate_integration, api_key_required=True, authorization_type=aws_apigateway.AuthorizationType.NONE)
        api.root.resource_for_path("login").add_method("POST", register_authenticate_integration, api_key_required=True, authorization_type=aws_apigateway.AuthorizationType.NONE)
        
        # Crear un plan de uso para el API Gateway y una clave de API
        plan = api.add_usage_plan("UsagePlan",
                                  name="MoviesAppUsagePlan",
                                  api_stages=[{"api": api, "stage": api.deployment_stage}],
                                 )
        
        # Crea una clave de API para el plan de uso
        key = api.add_api_key("MoviesAppKey")
        

        # Asegúrate de dar los permisos necesarios a las funciones Lambda para acceder a RDS
        database.grant_connect(register_authenticate_lambda)
        database.grant_connect(create_admin_lambda)