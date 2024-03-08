import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instances = ec2.instances.all()
        
    # Construir una lista de instancias con atributos específicos
    instances_data = [
        instance.instance_id for instance in instances
    ]
    
    return {
        'statusCode': 200,
        'body': json.dumps(instances_data)
    }

    
  
