from django.shortcuts import render
from django.http import JsonResponse
from storages.backends.s3boto3 import S3Boto3Storage
import json

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
    directory = 'TMDB/detail/2023-09-01/'  # 원하는 디렉토리 경로

    # 디렉토리 내의 모든 파일 목록 가져오기
    directories, files = storage.listdir(directory)

    movie_details = []  # 모든 영화의 세부 정보를 저장할 리스트

    for file_name in files:
        json_file = storage.open(f"{directory}/{file_name}")
        data = json_file.read()
        json_file.close()
        decoded_data = json.loads(data.decode('utf-8'))
        original_title = decoded_data["original_title"]
        poster_path = decoded_data["poster_path"]
        movie_details.append({"movie_title": original_title, "movie_poster": poster_path})

    return render(request, 'sms_site/dictionary.html', {"movie_details": movie_details})

def home(request):
    return render(request, "sms_site/home.html")