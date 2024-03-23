import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):
    movie_id = 787699
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US'

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer <TOKEN>"
    }

    response = requests.get(url, headers=headers)
    movie_data = response.json()
    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    table = dynamodb.Table('MoviesTable')
    
    table.put_item(
        Item={
            "movie_id": f'{movie_id}',
            "title": movie_data["original_title"],
            "year": movie_data["release_date"].split("-")[0],
            "genre": movie_data["genres"][0]["name"],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    
if __name__ == "__main__":
    lambda_handler(None, None)