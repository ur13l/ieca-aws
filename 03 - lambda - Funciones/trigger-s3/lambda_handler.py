# Trigger executed once a file is uploaded to the S3 bucket to store a JSON file with the metadata of the uploaded file
import boto3
import json

DEST_BUCKET = 'mybucket-ieca-uriel'

def lambda_handler(event, context):
    
    # Get the bucket name and the file name
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    print(event)
    
    # Get the metadata of the file
    s3 = boto3.client('s3')
    head_object = s3.head_object(Bucket=bucket, Key=file_name)
    
    

    # Store the metadata in a JSON file
    with open('/tmp/metadata.json', 'w') as file:
        file.write(json.dumps(head_object['Metadata']))
    
    
    
    s3.upload_file('/tmp/metadata.json', DEST_BUCKET, f'{file_name}-metadata.json')
    
    return {
        'statusCode': 200,
        'body': 'Metadata stored'
    }
    