import json
import boto3

def lambda_handler(event, _context):
    instance_id = event['body']['instance_id']
    action = event['body']['action']
    
    if not instance_id:
        return {
            'statusCode': 400,
            'body': json.dumps('Se requiere el ID de la instancia')
        }
    
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    instance = ec2.Instance(instance_id)
    
    # check if instance exists
    if not instance:
        return {
            'statusCode': 400,
            'body': json.dumps('La instancia no existe')
        }
    
    if action == 'stop':
        # Check if instance is running
        if instance.state['Name'] == 'running'  :
            instance.stop()
            return {
                'statusCode': 200,
                'body': json.dumps('Instancia detenida')
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('La instancia no está en ejecución')
            }
    
    elif action == 'start':
        # Check if instance is stopped
        if instance.state['Name'] == 'stopped':
            instance.start()
            return {
                'statusCode': 200,
                'body': json.dumps('Instancia iniciada')
            }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps('La instancia no está detenida')
            }

  
