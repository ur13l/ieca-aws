import os
import requests
import boto3
import json
from datetime import datetime


def upload_poster(movie_data, bucket_name):
    s3 = boto3.client('s3')
    poster_path = movie_data["poster_path"]
    poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
    key = f'{movie_data["id"]}.jpg'
    
    response = requests.get(poster_url)
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=response.content,
        ContentType='image/jpeg'
    )
    
    return key

def register_movie(movie_id, movie_data, poster_key, table_name):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(table_name)
    item = {
            "movie_id": f'{movie_id}',
            "title": movie_data["original_title"],
            "year": int(movie_data["release_date"].split("-")[0]),
            "genre": movie_data["genres"][0]["name"],
            "poster_key": poster_key,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    table.put_item(
        Item=item
    )
    
    return item

def handler(event, context):
    table_name = os.environ["MOVIES_TABLE"]
    bucket_name = os.environ["POSTER_BUCKET"]
    method = event["httpMethod"]
    
    if method == "POST":
        body = json.loads(event["body"])
        movie_id = body.get("movie_id", None)
        if not movie_id:
            return {
                "statusCode": 400,
                "body": "movie_id es requerido"
            }
        
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer <TMDB_TOKEN>"
        }

        response = requests.get(url, headers=headers)
        movie_data = response.json()
        
        key = upload_poster(movie_data, bucket_name)
        
        item = register_movie(movie_id, movie_data, key, table_name)
        
        if response.status_code != 200:
            return {
                "statusCode": 404,
                "body": "No se encontró la película"
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    
    elif method == "GET":
        movie_id = event["pathParameters"]["movie_id"]
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table(table_name)
        
        response = table.get_item(
            Key={
                "movie_id": movie_id
            }
        )
        
        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": "No se encontró la película"
            }
        
        item = response["Item"]
        
        s3 = boto3.client('s3')
        
        item['year']=int(item['year'])
        item['poster_url'] = s3.generate_presigned_url('get_object',
                                                      Params={'Bucket': bucket_name,
                                                              'Key': item['poster_key']},
                                                      ExpiresIn=3600)
        
        return {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    
   
    
    