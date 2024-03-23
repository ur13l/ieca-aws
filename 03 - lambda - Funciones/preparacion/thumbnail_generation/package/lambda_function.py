import os
import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')

def is_image_format_supported(filename):
    supported_formats = ['jpg', 'jpeg', 'png']
    return any(filename.lower().endswith(f".{fmt}") for fmt in supported_formats)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        # Determinar si la imagen ya tiene una miniatura prefijo /thumbnail
        if key.startswith("thumbnails/"):
            print(f"Thumbnail already exists.")
            return
        
        if not is_image_format_supported(key):
            print(f"File format not supported for {key}.")
            return
        
       
        
        # Descargar la imagen del bucket S3
        file_obj = s3_client.get_object(Bucket=bucket, Key=key)
        file_content = file_obj['Body'].read()
        
        # Procesar la imagen y crear una miniatura
        with Image.open(io.BytesIO(file_content)) as img:
            img.thumbnail((128, 128))
            buffer = io.BytesIO()
            img.save(buffer, 'JPEG')
            buffer.seek(0)
            
            # Subir la miniatura de vuelta al S3
            s3_client.upload_fileobj(buffer, bucket, f"thumbnails/{key}")
            print(f"Thumbnail created and uploaded for {key}.")
            
            
            
