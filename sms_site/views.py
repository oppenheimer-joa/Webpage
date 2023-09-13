from django.shortcuts import render
from configparser import ConfigParser
from storages.backends.s3boto3 import S3Boto3Storage
import json
from django.db.models import Q
import pandas as pd
import boto3
from io import BytesIO
import pyarrow.parquet as pq

    
def dictionary(request):

    parser = ConfigParser()
    parser.read("./config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/2023-07-14/')


    movie_details = pd.DataFrame(columns=[
        'id', 'cast', 'crew', 'backdrop_path', 'belongs_to_collection',
        'budget', 'genres', 'homepage', 'imdb_id', 'original_language',
        'original_title', 'overview', 'poster_path', 'production_companies',
        'production_countries', 'release_date', 'revenue', 'runtime',
        'spoken_languages', 'video', 'results', 'backdrops', 'logos',
        'posters'
    ])

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        print(file_path)
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_data = BytesIO(s3_object['Body'].read())
        parquet_table = pq.read_table(parquet_data)
        parquet_df = parquet_table.to_pandas()
        movie_details = pd.concat([movie_details, parquet_df], ignore_index=True)

    # 장르 endpoint 가 붙으면
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='genre/2023-07-14/')

    genre_df = pd.DataFrame()

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        print(file_path)
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_data = BytesIO(s3_object['Body'].read())
        parquet_table = pq.read_table(parquet_data)
        parquet_df = parquet_table.to_pandas()
        genre_df = pd.concat([genre_df, parquet_df], ignore_index=True)
        
    movie_by_genre_list = genre_df[genre_df['Drama'] == 1]['id'].tolist()
    # 장르 endpoint 코드 끝

    search_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    if search != "": # search 값이 있으면
        if search_type == '제목' :
            movie_details = movie_details[movie_details['original_title'].str.contains(search)]
        if search_type == '내용' :
            movie_details = movie_details[movie_details['overview'].str.contains(search)]
        if search_type == '감독' :
            movie_details = movie_details
    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_details,
                                                       "search":search,
                                                       "search_type":search_type})


def genre_list(request):
    return render(request, "sms_site/dictionary_genre.html")

def movie_filter_by_genre(request,genre):

    parser = ConfigParser()
    parser.read("./config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='genre/2023-07-14/')

    genre_df = pd.DataFrame()

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        print(file_path)
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_data = BytesIO(s3_object['Body'].read())
        parquet_table = pq.read_table(parquet_data, filters=[(id,'=',1)])
        parquet_df = parquet_table.to_pandas()
        genre_df = pd.concat([genre_df, parquet_df], ignore_index=True)
        
    movie_by_genre_list = genre_df[genre_df['Drama'] == 1]['id'].tolist()


    return render(request, "sms_site/dictionary.html")

def home(request):
    return render(request, "sms_site/home.html")

