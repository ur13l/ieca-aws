import json
import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instances = ec2.instances.all()
        
    # Construir una lista de instancias con atributos específicos
    instances_data = [
        {
            'instance_id': instance.instance_id,
            'status': instance.state['Name'],
            'name': next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), "Sin nombre"),
        } for instance in instances
    ]
    
    return {
        'statusCode': 200,
        'body': instances_data
    }

    
  
