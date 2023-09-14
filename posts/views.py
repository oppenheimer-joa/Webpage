def dataframe_confirm(dataframe, column):
    try : return_value = dataframe.iloc[0][column]
    except Exception as e :
        print(e)
        return_value = "ERROR"
    return return_value

def main(request):
    from django.shortcuts import render, redirect
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    if not is_authenticated:
        return redirect('/users/login')

    return render(request, 'posts/DEMO-select.html')

def movies(request):
    from django.shortcuts import render, redirect
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    if not is_authenticated:
        return redirect('/users/login')

    return render(request, 'posts/DEMO-movies.html')

# 조회할 데이터 : 단일 영화의 전역 정보
def movies_detail(request, pk):
    from django.shortcuts import render, get_object_or_404, redirect
    from .models import ExternalImageModel
    from configparser import ConfigParser
    import boto3
    import json
    import pandas as pd
    import pyarrow.parquet as pq
    from io import BytesIO

    parser = ConfigParser()
    parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access,
    aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/1960-01-01/')
    
    combined_df = pd.DataFrame()
    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_stream = s3_object['Body'].read()
        table = pq.read_table(BytesIO(parquet_stream))
        df = table.to_pandas()
        new_df = pd.concat([combined_df, df])

    row = new_df[new_df['id'] == pk]

    movie_id = dataframe_confirm(row, 'id')
    movie_nm = dataframe_confirm(row, 'original_title')
    movie_dt = dataframe_confirm(row, 'overview')
    movie_gr = dataframe_confirm(row, 'genres')
    poster_path_str = dataframe_confirm(row, 'posters')
    date = dataframe_confirm(row, 'release_date')
    backdrop_path_str = dataframe_confirm(row, 'backdrop_path')

    # read genre json file
    json_path = "/home/neivekim76/demo/json/genre.json"
    with open(json_path, 'r') as file:
        data = json.load(file)
    json_genre = data["genres"]

    # parse genre
    genre_string = ""
    for genre_id in movie_gr:
        for genre_reference in json_genre:
            if genre_id == genre_reference['id']:
                genre_string += f"{genre_reference['name']}, "

    try: 
        url_poster = f"https://image.tmdb.org/t/p/original{poster_path_str}"
    except Exception as e: 
        url_poster = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"


    try: 
        url_backdrop = f"https://image.tmdb.org/t/p/original{backdrop_path_str}"
    except Exception as e: 
        url_backdrop = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"


    context = {
        'movie_id' : movie_id,
        'movie_nm' : movie_nm,
        'movie_dt' : movie_dt,
        'movie_gr' : genre_string[:-2],
        'poster' : url_poster,
        'external_image' : url_backdrop,
        'date' : date
    }

    return render(request, 'posts/DEMO-movies-detail.html', context)
