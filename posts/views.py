def dataframe_confirm(dataframe, column):
    try : return_value = dataframe.iloc[0][column]
    except : return_value = "ERROR"
    return return_value

def main(request):
    from django.shortcuts import render, redirect
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    if not is_authenticated:
        return redirect('/users/login')

    return render(request, 'posts/DEMO-main.html')

# 조회할 데이터 : 단일 영화의 전역 정보
def external_image_detail(request, pk):
    from django.shortcuts import render
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
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/2023-07-14/')
    
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
    # poster_path_str = dataframe_confirm(row, 'posters')
    poster_path_str = dataframe_confirm(row, 'backdrops')[0]['file_path']

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
        poster_path = f"https://image.tmdb.org/t/p/original{poster_path_str}"
        external_image, created = ExternalImageModel.objects.get_or_create(pk=pk, defaults={'image_url': poster_path})
        url = external_image.image_url

    except Exception as e: 
        print(f"An error occurred: {str(e)}")
        url = "https://image.tmdb.org/t/p/original/9Yg7DZE4ip2Yl0K2BUm6hAd8iRK.jpg"

    context = {
        'movie_id' : movie_id,
        'movie_nm' : movie_nm,
        'movie_dt' : movie_dt,
        'movie_gr' : genre_string[:-2],
        'external_image' : url
    }

    return render(request, 'posts/external_image_detail.html', context)
