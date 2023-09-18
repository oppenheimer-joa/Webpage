from django.shortcuts import render
from configparser import ConfigParser
from storages.backends.s3boto3 import S3Boto3Storage
import json
from django.db.models import Q
import pandas as pd
import boto3
from io import BytesIO
import pyarrow.parquet as pq
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    
def dictionary(request):
    # genre list 변수
    genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
        'Romance', 'Science_Fiction', 'TV_Movie', 'Thriller', 'War', 'Western',
        'id']
    
    # request GET
    search_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'recent')

    # s3 연동
    parser = ConfigParser()
    # parser.read("./config/config.ini")
    parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    
    # movie 정보 가져오기
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/')
    movie_details = pd.DataFrame()
    
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


    # 페이지 기능 구현
    # 데이터프레임은 페이지 기능이 어려우니 to_dict를 이용해서 레코드 한 줄씩 리스트로 변환
    movie_list = movie_details.to_dict('records')
    paginator = Paginator(movie_list, 20)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
        
    # 장르 endpoint 가 붙으면
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB_genre/')

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
        if search_type == 'title' :
            movie_details = movie_details[movie_details['original_title'].str.contains(search)]
        if search_type == 'director' :
            movie_details = movie_details
    # 리턴값에 'pages': pages 추가  
    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_list,
                                                       "search":search,
                                                       "search_type":search_type,
                                                       'pages': pages})

def movie_filter_by_genre(request):
    genre = request.GET.get('genre', '')

    parser = ConfigParser()
    parser.read("./config/config.ini")
    # parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB_genre/')

    genre_df = pd.DataFrame()
    genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
       'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
       'Romance', 'Science_Fiction', 'TV_Movie', 'Thriller', 'War', 'Western',
       'id']

    for obj in objects.get('Contents'):
        file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
        print(file_path)
        if file_path.find('parquet') == -1:
            continue
        s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
        parquet_data = BytesIO(s3_object['Body'].read())
        parquet_table = pq.read_table(parquet_data, filters=[(genre,'=',1)])
        parquet_df = parquet_table.to_pandas()
        genre_df = pd.concat([genre_df, parquet_df], ignore_index=True)

        movie_id_in_genre = genre_df['id'].tolist()
        movie_id_in_genre = list(map(int,movie_id_in_genre))

    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/')
    movie_details = pd.DataFrame()

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

    movie_genre_details = movie_details[movie_details['id'].isin(movie_id_in_genre)]
    if movie_genre_details.shape[0] == 0 :
        return render(request, 'sms_site/dictionary.html',{"no_filter": "조건에 맞는 결과가 없습니다",
                                                           "selected_genre": genre,
                                                            "genre_list":genre_list})
    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_genre_details,
                                                       "selected_genre": genre,
                                                       "genre_list":genre_list})


def performance(request):
    return render(request, 'sms_site/performance.html')

def home(request):
    return render(request, "sms_site/home.html")
