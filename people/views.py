from django.shortcuts import render
from configparser import ConfigParser
from storages.backends.s3boto3 import S3Boto3Storage
import json, requests
from django.db.models import Q
import pandas as pd
import boto3, re
from io import BytesIO
import pyarrow.parquet as pq
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import duckdb, os

    
def dictionary(request):
    # # department list 변수
    # department_list = ['Acting', 'Production', 'Sound', 'Directing', 'Writing', 'Editing',
    #    'Crew', 'Visual Effects', 'Camera', 'Lighting',
    #    'Costume & Make-Up', 'Art', 'Creator']
    
    # request GET
    search = request.GET.get('search', '')
    department = request.GET.get('department', '')
    sort_by = request.GET.get('sort', 'name_asc')
    
    # sort_by 값에 따라 SQL 정렬 구문 생성
    order_by_clause = "ORDER BY name ASC" if sort_by == 'name_asc' else "ORDER BY name DESC" if sort_by == 'name_dsc' else ""

    # search 및 department 값에 따라 SQL 필터 구문 생성
    where_clauses = []
    if search:
        where_clauses.append(f"name LIKE '%{search}%'")
    if department:
        where_clauses.append(f"known_for_department = '{department}'")
    where_clause = " AND ".join(where_clauses)
    where_clause = f"WHERE {where_clause}" if where_clause else ""
    
    QUERY = f'''
                SELECT 
                    id, date_gte, name, 
                    known_for_department, profile_img, 
                    birth, death
                FROM 
                    tmdb_people 
                {where_clause}
                {order_by_clause}
                '''
    print("QUERY")
    print(QUERY)

    # database 절대 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, f'../database/tmdb')
    
    # DuckDB에 연결
    conn = duckdb.connect(database=database_dir, read_only=False)

    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(QUERY)

    # 결과 가져오기
    result_all = cursor.fetchall()

    # 컬럼 이름 지정
    columns = ['id', 'date_gte', 'name', 'known_for_department', 'profile_img', 'birth', 'death']

    # 결과를 딕셔너리 리스트로 변환
    dict_list = [dict(zip(columns, row)) for row in result_all]

    # 연결 종료
    conn.close()

    # 페이지 기능 구현
    paginator = Paginator(dict_list, 20)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)
        
    # 리턴값에 'pages': pages 추가 
    return render(request, 'people/dictionary.html',{"selected_department": department,
                                                    'sort_by':sort_by,
                                                    "search":search,
                                                    'pages': pages})
    
def people_info(request, id):
    
    # database 절대 경로 반환
    current_dir = os.path.dirname(os.path.abspath(__file__))
    database_dir = os.path.join(current_dir, f'../database/tmdb')
    
    # DuckDB에 연결
    conn = duckdb.connect(database=database_dir, read_only=False)

    # 쿼리 실행
    cursor = conn.cursor()
    cursor.execute(f'''
                SELECT 
                    id, date_gte, name, 
                    known_for_department, profile_img, 
                    birth, death
                FROM 
                    tmdb_people
                WHERE id = {id}
                ''')

    # 결과 가져오기
    result_all = cursor.fetchall()

    # 컬럼 이름 지정
    columns = ['id', 'date_gte', 'name', 'known_for_department', 'profile_img', 'birth', 'death']

    # 결과를 딕셔너리 리스트로 변환
    dict_list = [dict(zip(columns, row)) for row in result_all]

    # 연결 종료
    conn.close()

    parser = ConfigParser()
    parser.read("./config/config.ini")
    api_key = parser.get("TMDB", "API_KEY_1")
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
    count = len(filtered_movies)
    # 페이지 기능 구현
    paginator = Paginator(filtered_movies, 20)
    # 한 페이지에 보여줄 컨텐츠 수 지정(ex : 5개면 ('page', 5))
    page = request.GET.get('page', 1)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(1)

    return render(request, 'people/people_info.html', {'person_info':dict_list[0], 'pages':pages, 'count':count})
    




