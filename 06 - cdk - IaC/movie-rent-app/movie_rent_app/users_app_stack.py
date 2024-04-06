from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    aws_ec2 as ec2,
    aws_rds as rds,
    # aws_sqs as sqs,
)
from constructs import Construct

class UsersAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Define una red VPC para alojar tu base de datos
        vpc = ec2.Vpc.from_lookup(self, "VPC",
            is_default=True
        )
        
        # Crear un nuevo grupo de seguridad
        security_group = ec2.SecurityGroup(self, "SecurityGroupPostgres",
                                               vpc=vpc,
                                               description="Permite acceso a RDS desde una IP especifica",
                                               allow_all_outbound=True
                                               )

        # Añadir una regla de entrada para permitir el tráfico PostgreSQL desde una IP específica
        security_group.add_ingress_rule(peer=ec2.Peer.ipv4('189.203.206.218/32'),
                                        connection=ec2.Port.tcp(5432),
                                        description="Acceso PostgreSQL")
        

        # Crea una base de datos PostgreSQL en RDS utilizando configuraciones elegibles para la capa gratuita
        database = rds.DatabaseInstance(self, "UserDatabase",
                                            engine = rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_16),
                                            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
                                            vpc=vpc,
                                            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                                            allocated_storage=20, # Configura hasta 20 GB, que es el límite para la capa gratuita
                                            max_allocated_storage=20, # Opcional, para prevenir el auto escalado
                                            deletion_protection=False, # Considera habilitar en producción
                                            credentials=rds.Credentials.from_generated_secret("user_admin"), # Usa credenciales seguras
                                            database_name="users_db", # Nombre de tu base de datos
                                            security_groups=[security_group], # Asigna el grupo de seguridad
                                            multi_az=False,
                                            publicly_accessible=True,
                                           )
        