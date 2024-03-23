import json
import boto3
import os
import traceback

ec2 = boto3.resource('ec2', region_name=os.environ.get('REGION_NAME'))

def lambda_handler(event, context):
    try: 
        method = event['httpMethod']
        
        if method == 'GET':
            instances = ec2.instances.all()
            
            instancesData = [
                {
                    "InstanceId": instance.instance_id,
                    "State": instance.state['Name'],
                    "Name":  next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), "Sin nombre"),
                    "PublicIP": instance.public_ip_address
                } 
                for instance in instances
            ]
            
            return {
                'statusCode': 200,
                'body': instancesData
            }
        
        elif method == 'POST':
            instance_id = event['body']['instance_id']
            action = event['body']['action']
            
            instance = ec2.Instance(instance_id)
            if not instance:
                return {
                    'statusCode': 404,
                    'message': 'La instancia no fue encontrada'
                }
            
            if action == 'start' and instance.state['Name'] == 'stopped':
                instance.start()
                return {
                    'statusCode': 200,
                    'body': {
                        'message': f'La instancia {instance.instance_id} fue iniciada correctamente.'
                    }
                }
            elif action == 'stop' and instance.state['Name'] == 'running':
                instance.stop()
                return {
                    'statusCode': 200,
                    'body': {
                        'message':f'La instancia {instance.instance_id} fue detenida correctamente'
                    }
                }
            
            return {
                'statusCode': 400,
                'message': f'La instancia se encuentra en estado {instance.state['Name']}, y no puede ejecutar la acción {action}'
            }
        
    except Exception as e:
        traceback.print_exc()
        return {
            'statusCode': 400,
            'message': 'La petición no se puede completar, revise su información de envío'
        }
