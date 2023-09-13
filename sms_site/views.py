from django.shortcuts import render
from django.http import JsonResponse
from storages.backends.s3boto3 import S3Boto3Storage
import json
from django.db.models import Q
import pandas as pd
import io

# Create your views here.
# def index(request):
#     storage = S3Boto3Storage()
#     json_file = storage.open('TMDB/detail/2023-01-06/TMDB_movieDetails_1001800_2023-01-06.json')
#     data = json_file.read()
#     # JSON 데이터 디코딩
#     decoded_data = json.loads(data.decode('utf-8'))

#     original_title = decoded_data["original_title"]
#     poster_path = decoded_data["poster_path"]
#     json_file.close()
#     return render(request, 'index.html', {"movie_title": original_title, "movie_poster": poster_path})

def dictionary(request):
    storage = S3Boto3Storage()
    directory = 'TMDB/2023-07-14/TMDB_movie_872585_2023-07-14'  # 원하는 디렉토리 경로

    # 디렉토리 내의 모든 파일 목록 가져오기
    directories, files = storage.listdir(directory)
    print(files)

    movie_details = pd.DataFrame(columns=[
        'id', 'cast', 'crew', 'backdrop_path', 'belongs_to_collection',
       'budget', 'genres', 'homepage', 'imdb_id', 'original_language',
       'original_title', 'overview', 'poster_path', 'production_companies',
       'production_countries', 'release_date', 'revenue', 'runtime',
       'spoken_languages', 'video', 'results', 'backdrops', 'logos',
       'posters'
    ])  # 일단 인물 정보로 parquet test

    for idx, file_name in enumerate(files):
        if file_name == '_SUCCESS' :
            continue
        file = storage.open(f"{directory}/{file_name}")
        pq_file = pd.read_parquet(file)
        movie_details = pd.concat([movie_details, pq_file], ignore_index=True)
        # data = json_file.read()
        # json_file.close()
        # decoded_data = json.loads(data.decode('utf-8'))
        # original_title = decoded_data["original_title"]
        # poster_path = decoded_data["poster_path"]
        # movie_details.append({"movie_title": pq_file})
        if idx >= 30 :
            break
    
    search = request.GET.get('search', '')
    if search: # search 값이 있으면
        movie_details = [movie for movie in movie_details if search in movie["movie_title"]]
    return render(request, 'sms_site/dictionary.html',{"movie_list": movie_details})



def home(request):
    return render(request, "sms_site/home.html")

