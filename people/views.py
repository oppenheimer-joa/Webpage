from django.shortcuts import render
from configparser import ConfigParser
from storages.backends.s3boto3 import S3Boto3Storage
import json, requests
from django.db.models import Q
import pandas as pd
import boto3
from io import BytesIO
import pyarrow.parquet as pq
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

    
def dictionary(request):

    parser = ConfigParser()
    parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/people_info/')
    
    people_details = pd.DataFrame(columns=[
        'id', 'date_gte', 'name', 'known_for_department', 'profile_img', 'birth', 'death'
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
        people_details = pd.concat([people_details, parquet_df], ignore_index=True)
    
    # 중복된 'id'를 가진 행 제거 (처음 발견되는 것만 남김)
    people_details.drop_duplicates(subset=['id'], keep='first', inplace=True)

    # 페이지 기능 구현
    # 데이터프레임은 페이지 기능이 어려우니 to_dict를 이용해서 레코드 한 줄씩 리스트로 변환
    people_list = people_details.to_dict('records')
    paginator = Paginator(people_list, 1)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
        
    search = request.GET.get('search', '')
    if search != "": # search 값이 있으면
        people_details = people_details
    # 리턴값에 'pages': pages 추가 
    return render(request, 'people/dictionary.html',{"people_list": people_list,
                                                       "search":search,
                                                       'pages': pages})
    
def people_info(request, id):
    parser = ConfigParser()
    parser.read("/home/neivekim76/config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")

    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/people_info/')
    
    people_details = pd.DataFrame(columns=[
        'id', 'date_gte', 'name', 'known_for_department', 'profile_img', 'birth', 'death'
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
        people_details = pd.concat([people_details, parquet_df], ignore_index=True)
        
    # 중복된 'id'를 가진 행 제거 (처음 발견되는 것만 남김)
    people_details.drop_duplicates(subset=['id'], keep='first', inplace=True)
    
    # 특정 ID 사람의 정보만 뽑기
    selected_person = people_details.loc[people_details['id'] == int(id)]

    # DataFrame을 딕셔너리로 변환
    if not selected_person.empty:
        selected_person_dict = selected_person.to_dict('records')[0]
    else:
        selected_person_dict = {}  # 해당 ID가 없을 경우 빈 딕셔너리를 사용
        
    api_key = parser.get("TMDB", "API_KEY")
    base_url = f'https://api.themoviedb.org/3/person/{id}/movie_credits'
    headers = {
    	"Authorization": f"Bearer {api_key}",
    	"accept": "application/json"
    }
    
    response = requests.get(base_url, headers=headers)
    resp_status_check = response.status_code
    if resp_status_check == 200:
        json_data = response.json()
        
    # 필요한 정보만 추려서 새로운 리스트 생성
    filtered_movies = []

    # 'data'는 원래의 JSON 데이터를 담고 있는 딕셔너리라고 가정합니다.
    for key in ['cast', 'crew']:
        if key in json_data and json_data[key]:  # 해당 키가 있고, 값이 비어 있지 않은 경우
            for movie in json_data[key]:
                filtered_movie = {
                    'id': movie['id'],
                    'overview': movie.get('overview', ''),  # 'get' 메서드를 사용하면 해당 키가 없을 경우에도 처리 가능
                    'poster_path': movie.get('poster_path', ''),
                    'original_title': movie.get('original_title', ''),
                    'release_date': movie.get('release_date', '')
                }
                filtered_movies.append(filtered_movie)
    # 페이지 기능 구현
    paginator = Paginator(filtered_movies, 4)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    return render(request, 'people/people_info.html', {'person_info':selected_person_dict, 'pages':pages})
    




