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
    
    # table.put_item(
    #     Item={
    #         "movie_id": f'{movie_id}',
    #         "title": movie_data["original_title"],
    #         "year": movie_data["release_date"].split("-")[0],
    #         "genre": movie_data["genres"][0]["name"],
    #         "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     }
    # )
    
    # Obtener una película por su PK (movie_id)
    # movie1 = table.get_item(
    #     Key={
    #         "movie_id": "787699"
    #     }
    # )
    # print(movie1)
    
    
    # Obtener todas las películas con scan
    # all_movies = table.scan(
    #     FilterExpression=boto3.dynamodb.conditions.Attr('year').eq('2024')
    #         .__and__(boto3.dynamodb.conditions.Attr('title').begins_with('Godzilla')),
    # )
    
    filter_movies = table.scan(
        FilterExpression="#year_attr = :year AND begins_with(#title, :title)",
        ExpressionAttributeValues={
            ":title": "Godzilla",
            ":year": "2024"
        },
        ExpressionAttributeNames={
            "#year_attr": "year",
            "#title": "title"
        }
    )
    
    # Obtener películas por género
    movies_by_genre = table.query(
        IndexName='GSI_Genre',
        KeyConditionExpression="#genre = :genre",
        FilterExpression="#year = :year AND begins_with(#title, :title)",
        ExpressionAttributeValues={
            ":genre": "Action",
            ":year": "2024",
            ":title": "Godzilla"
        },
        ExpressionAttributeNames={
            "#genre": "genre",
            "#year": "year",
            "#title": "title"
        }
    )
    
    print(movies_by_genre)
    
    
    
if __name__ == "__main__":
    lambda_handler(None, None)