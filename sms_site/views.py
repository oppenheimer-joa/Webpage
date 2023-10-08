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
    import os, duckdb

    # genre list 변수
    genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
        'Romance', 'Science_Fiction', 'TV_Movie', 'Thriller', 'War', 'Western',
        'id']
    
    genre_dict = {'Action' : '28', 'Adventure' : '12', 'Animation' : '16', 'Comedy' : '35', 
                  'Crime' : '80', 'Documentary' : '99', 'Drama' : '18', 'Family' : '10751', 
                  'Fantasy' : '14', 'History' : '36', 'Horror' : '27', 'Music' : '10402', 
                  'Mystery' : '9648', 'Romance' : '10749', 'Science_Fiction' : '878', 'TV_Movie' : '10770',
                  'Thriller' : '53', 'War' : '10752', 'Western' : '37'} 
    
    # request GET
    search_type = request.GET.get('type', '')
    search = request.GET.get('search', '')
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'recent')
    date = request.GET.get('date', '')

    ######################################################################################################

    # database 절대 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, f'../database/tmdb')

    QUERY = '''
            SELECT 
                id, original_title, overview, posters,
                backdrop_path, release_date, "cast", crew,
                belongs_to_collection, budget, production_companies, production_countries,
                revenue, runtime, genres
            FROM 
                tmdb_movie
            '''

    # 장르 endpoint 가 붙으면
    if genre != "" :

        QUERY += f'''
                 WHERE
                     ARRAY_CONTAINS(genres, {genre_dict[genre]}) 
                 '''

    # 검색 엔진이 붙으면
    if search != "":
        if search_type == 'title' :
            if genre == "":
                QUERY += f"WHERE original_title LIKE '%{search}%'"
            else:
                QUERY += f"AND original_title LIKE '%{search}%'"

        if search_type == 'country' :
            if genre == "":
                QUERY += f'''
                        WHERE EXISTS (
                            SELECT 1 
                            FROM UNNEST(production_countries) AS c 
                            WHERE c.name = 'f{search}'
                        ) 
                        '''
            else:
                QUERY += f'''
                        AND EXISTS (
                            SELECT 1 
                            FROM UNNEST(production_countries) AS c 
                            WHERE c.name = 'f{search}'
                        ) 
                        '''

    # sort 조건이 붙으면
    if sort_by != "": 
        if sort_by == 'recent' :
            QUERY += 'ORDER BY release_date DESC '
        elif sort_by == 'old' :
            QUERY += 'ORDER BY release_date ASC '

    ################################################################################################################################################            

    # DuckDB에 연결
    conn = duckdb.connect(database=database_dir, read_only=False)  

    # 쿼리 실행 - cast 목록 반환
    cursor = conn.cursor()
    cursor.execute(QUERY)
    
    # 결과 가져오기
    fetched = cursor.fetchall()
    conn.close()

    column_list = ['id', 'original_title', 'overview', 'posters',
                'backdrop_path', 'release_date', '"cast"', 'crew',
                'belongs_to_collection', 'budget', 'production_companies', 'production_countries',
                'revenue', 'runtime', 'genres']
    
    movie_list = [{col: val for col, val in zip(column_list, movie)} for movie in fetched]

    # print("SHOW MOVIE LIST <<<<<<<<<<<<<<<<< ")
    # print(movie_list)

    paginator = Paginator(movie_list, 20)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)


    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_list,
                                                       "search":search,
                                                       "search_type":search_type,
                                                       'sort_by':sort_by,
                                                       "genre_list":genre_list,
                                                       "selected_genre":genre,
                                                       'pages': pages})



def performance(request):
    import os, duckdb

    # request GET
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort', 'recent')
    search_type = request.GET.get('type', '')
    search = request.GET.get('search', '')

    # database 절대 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, f'../database/kopis')

    QUERY = '''
            SELECT 
                *
            FROM 
                performance
            '''  

    # 장르 변수
    genre_dict = {'':'', 'theater':'연극', 'musical':'뮤지컬', 'classic':'서양음악(클래식)', 'korean':'한국음악(국악)', 'popular':'대중무용/대중음악', 'dance':'무용(서양무용/한국무용)', 'extra':'기타'}
    if genre != "" :
        QUERY += f"""
                 WHERE
                     genrenm = '{genre_dict[genre]}'
                 """

    if search != "": # search 값이 있으면
        if search_type == "title":
            if genre == "":
                QUERY += f"WHERE prfnm LIKE '%{search}%'"
            else:
                QUERY += f"AND prfnm LIKE '%{search}%'"

        elif search_type == "location":
            if genre == "":
                QUERY += f"WHERE fcltynm LIKE '%{search}%'"
            else:
                QUERY += f"AND fcltynm LIKE '%{search}%'"

            
    if sort_by != "": # sort_by 값이 있으면
        if sort_by == 'open' :
            QUERY += 'ORDER BY prfpdfrom DESC '
        elif sort_by == 'close' :
            QUERY += 'ORDER BY prfpdto DESC '

    # DuckDB에 연결
    conn = duckdb.connect(database=database_dir, read_only=False)  

    # 쿼리 실행 - cast 목록 반환
    cursor = conn.cursor()
    cursor.execute(QUERY)
    
    # 결과 가져오기
    fetched = cursor.fetchall()
    conn.close()

    column_list = ['dtguidance', 'entrpsnm', 'fcltynm', 'genrenm', 
                   'mt10id', 'mt20id', 'openrun', 'pcseguidance', 
                   'poster', 'prfage', 'prfcast', 'prfcrew', 
                   'prfnm', 'prfpdfrom', 'prfpdto', 'prfruntime', 
                   'sty', 'styurls', 'tksites', 'genreCode']
    
    prf_list = [{col: val for col, val in zip(column_list, prf)} for prf in fetched]
    paginator = Paginator(prf_list, 18)

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


def prf_detail(request, id):
    import os, duckdb

    # database 절대 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, f'../database/kopis')

    # DuckDB에 연결
    conn = duckdb.connect(database=database_dir, read_only=False)  

    # 쿼리 실행 - cast 목록 반환
    cursor = conn.cursor()
    cursor.execute(f"""
                SELECT 
                    *
                FROM 
                   performance
                WHERE 
                   mt20id = '{id}'
                """)
    fetched = cursor.fetchall()[0]
    conn.close()

    column_list = ['dtguidance', 'entrpsnm', 'fcltynm', 'genrenm', 
                   'mt10id', 'mt20id', 'openrun', 'pcseguidance', 
                   'poster', 'prfage', 'prfcast', 'prfcrew', 
                   'prfnm', 'prfpdfrom', 'prfpdto', 'prfruntime', 
                   'sty', 'styurls', 'tksites', 'genreCode']
    
    prf_list = {col: val for col, val in zip(column_list, fetched)}

    return render(request, "sms_site/prf_detail.html", {"prf_info": prf_list,
                                                       "styurls": prf_list['styurls'],
                                                       "tksites": prf_list['tksites']})

def home(request):
    return render(request, "sms_site/home.html")
