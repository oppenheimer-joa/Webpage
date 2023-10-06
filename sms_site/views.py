from django.shortcuts import render
from configparser import ConfigParser
from storages.backends.s3boto3 import S3Boto3Storage
import json
from django.db.models import Q
import pandas as pd
import boto3
from io import BytesIO
import pyarrow.parquet as pq
from datetime import datetime
import ast
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


global prf_details

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
    date = request.GET.get('date', '')

    # s3 연동
    parser = ConfigParser()
    parser.read("config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    

    # movie 정보 가져오기
    # cache 가 있으면
    movie_details = cache.get('movie_details')
    print("캐시데이터 ::::: ", movie_details)

    if movie_details is None :

        objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB/2023-07-')
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
        # 캐시 데이터 저장
        cache.set('movie_details', movie_details, timeout=None)
    # 장르 endpoint 가 붙으면
    if genre != "" :
        s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
        objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix='TMDB_genre/2023-07-')

        genre_df = pd.DataFrame()

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
        movie_id_in_genre = list(map(int,movie_id_in_genre)) # 해당 장르의 영화 id list
        movie_details = movie_details[movie_details['id'].isin(movie_id_in_genre)]
        if movie_details.shape[0] == 0 :
            return render(request, 'sms_site/dictionary.html',{"no_filter": "조건에 맞는 결과가 없습니다",
                                                            "selected_genre": genre,
                                                            "genre_list":genre_list,
                                                            'search_type':search_type,
                                                            'search':search,
                                                            'sort_by':sort_by,
                                                            'pages': pages})

    if search != "": # search 값이 있으면
        if search_type == 'title' :
            movie_details = movie_details[movie_details['original_title'].str.contains(search)]
        if search_type == 'country' :
            # 나라에 대한 검색: 여기에서는 production_countries가 문자열 형태의 JSON이라고 가정합니다.
            def contains_country(row):
                try:
                    return any(country['name'] == search for country in row)
                except:
                    return False

            movie_details = movie_details[movie_details['production_countries'].apply(contains_country)]

    if date != "" :
        prf_details[['prfpdfrom','prfpdto']] = prf_details[['prfpdfrom','prfpdto']].applymap(lambda x : pd.to_datetime(x, format='%Y.%m.%d'))
        prf_details = prf_details[(prf_details['prfpdfrom'] <= date) & (date <= prf_details['prfpdto'])]


    if sort_by != "": # sort_by 값이 있으면
        if sort_by == 'recent' :
            movie_details = movie_details.sort_values(by='release_date', ascending=False)
        elif sort_by == 'old' :
            movie_details = movie_details.sort_values(by='release_date', ascending=True)
            
        
    # 페이지 기능 구현
    # 데이터프레임은 페이지 기능이 어려우니 to_dict를 이용해서 레코드 한 줄씩 리스트로 변환
    movie_list = movie_details.to_dict('records')
    print("SHOW MOVIE LIST <<<<<<<<<<<<<<<<< ")
    print(movie_list)

    paginator = Paginator(movie_list, 20)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)


    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_details,
                                                       "search":search,
                                                       "search_type":search_type,
                                                       'sort_by':sort_by,
                                                       "genre_list":genre_list,
                                                       "selected_genre":genre,
                                                       'pages': pages})



def performance(request):
    # request GET
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'recent')
    search_type = request.GET.get('type', '')
    search = request.GET.get('search', '')

    # 장르 변수
    genre_dict = {'':'', 'theater':'연극', 'musical':'뮤지컬', 'classic':'서양음악(클래식)', 'korean':'한국음악(국악)', 'popular':'대중무용/대중음악', 'dance':'무용(서양무용/한국무용)', 'extra':'기타'}

    # s3 연동
    parser = ConfigParser()
    parser.read("config/config.ini")
    access = parser.get("AWS", "S3_ACCESS")
    secret = parser.get("AWS", "S3_SECRET")
    s3 = boto3.client('s3', aws_access_key_id=access, aws_secret_access_key=secret)
    
    # prf 정보 가져오기
    # cache 가 있으면
    prf_details = cache.get('prf_details')
    print("캐시데이터 ::::: ", prf_details)
    # cache 가 없으면
    # prf 정보 가져오기
    if prf_details is None :
        objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix=f'kopis/2023/2023-07-1')
        prf_details = pd.DataFrame()

        for obj in objects.get('Contents'):
            file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
            if (file_path.find('parquet') == -1):
                continue
            print(file_path)
            s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
            parquet_data = BytesIO(s3_object['Body'].read())
            parquet_table = pq.read_table(parquet_data)
            parquet_df = parquet_table.to_pandas()
            prf_details = pd.concat([prf_details, parquet_df], ignore_index=True)
        # 캐시 데이터 저장
        prf_details[['prfpdfrom','prfpdto']] = prf_details[['prfpdfrom','prfpdto']].applymap(lambda x : datetime.strptime(x, '%Y.%m.%d'))
        cache.set('prf_details', prf_details, timeout=None)

    # 장르 검색
    if genre != "" : ## 찾으려는 genre 값이 있을 경우
        genre_df = pd.DataFrame()
        genre_objects = s3.list_objects_v2(Bucket='sms-warehouse', Prefix=f'kopis/2023/2023-07-1')
        for obj in genre_objects.get('Contents'):
            file_path = 's3://{}/{}'.format('sms-warehouse', obj.get('Key'))
            if (file_path.find('parquet') == -1) or (file_path.find(genre) == -1) :
                continue
            print(file_path)
            s3_object = s3.get_object(Bucket='sms-warehouse', Key=obj.get('Key'))
            parquet_data = BytesIO(s3_object['Body'].read())
            parquet_table = pq.read_table(parquet_data)
            parquet_df = parquet_table.to_pandas()
            genre_df = pd.concat([genre_df, parquet_df], ignore_index=True)
        prf_details = genre_df
        
        if prf_details.shape[0] == 0 :
            return render(request, 'sms_site/prf.html',{"no_filter": "조건에 맞는 결과가 없습니다",
                                                        'search_type':search_type,
                                                        'search':search,
                                                        'sort_by':sort_by,
                                                        "selected_genre": genre,
                                                        "selected_genre_nm": genre_dict[genre],
                                                        'pages': pages})
    if search != "": # search 값이 있으면
        if search_type == 'title' :
            prf_details = prf_details[prf_details['prfnm'].str.contains(search)]
        if search_type == 'location' :
            prf_details = prf_details[(prf_details['prfnm'].str.contains(search)) | (prf_details['fcltynm'].str.contains(search))]
            
    if sort_by != "": # sort_by 값이 있으면
        if sort_by == 'open' :
            prf_details = prf_details.sort_values(by='prfpdfrom', ascending=False)
        if sort_by == 'close' :
            prf_details = prf_details.sort_values(by='prfpdto') # 투표자순으로 배치 필요

    # 페이지 기능 구현
    # 데이터프레임은 페이지 기능이 어려우니 to_dict를 이용해서 레코드 한 줄씩 리스트로 변환
    prf_list = prf_details.to_dict('records')
    paginator = Paginator(prf_list, 18)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    return render(request, 'sms_site/prf.html',{
                                                'search_type':search_type,
                                                'search':search,
                                                'sort_by':sort_by,
                                                "selected_genre": genre,
                                                "selected_genre_nm": genre_dict[genre],
                                                'pages': pages})


def prf_detail(request,id):
    if id == "" :
        return performance(request)
    prf_details = cache.get('prf_details')
    print(prf_details)
    prf_details_id = prf_details[prf_details['mt20id'] == id].iloc[0]
    prf_details_id = prf_details_id.fillna("정보 없음")
    tklists = ast.literal_eval(prf_details_id['tksites'])
    print(tklists)

    ticket_lists = {}
    # 리스트 내의 각 dictionary를 하나로 합침
    for d in tklists:
        ticket_lists.update(d)
    print(ticket_lists)
    return render(request, "sms_site/prf_detail.html", {"prf_info": prf_details_id,
                                                       "styurls": prf_details_id['styurls'],
                                                       "tksites": ticket_lists})

def home(request):
    return render(request, "sms_site/home.html")
