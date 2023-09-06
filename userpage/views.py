from storages.backends.s3boto3 import S3Boto3Storage
from django.shortcuts import render
import json

# 임시 user movie
user_movie1 = {'movie_id' : '872585',
                'movie_dt' : '2023-07-14'}
user_movie2 = {'movie_id' : '250480',
                'movie_dt' : '1977-03-11'}  # 1977-03-11
user_movie3 = {'movie_id' : '569094',
                'movie_dt' : '2023-05-26'} # 2023-05-26

def get_data(movie_id, movie_dt) :
    storage = S3Boto3Storage()
    file_name = f"TMDB_movieDetails_{movie_id}_{movie_dt}.json"
    json_file = storage.open(f'TMDB/detail/{movie_dt}/{file_name}')
    print(json_file)
    data = json_file.read()
    decoded_data = json.loads(data.decode('utf-8'))
    return decoded_data

# Create your views here.
def userdetail(request) :
    context = {}
    user_info = request.session['login_session']
    context = {
        'user_nm': user_info,

        'user_movie1' : get_data(**user_movie1),
        'user_movie2' : get_data(**user_movie2),
        'user_movie3' : get_data(**user_movie3)
    }
    return render(request, 'userpage/userdetail.html', context)

def moviedetail(request,id) :
    storage = S3Boto3Storage()
    # 나중에 S3 읽어올 수 있을 때 수정...
    if id == '872585' :
        file_name = f"TMDB_movieDetails_{id}_2023-07-14.json"
        json_file = storage.open(f'TMDB/detail/2023-07-14/{file_name}')
    if id == '250480' :
        file_name = f"TMDB_movieDetails_{id}_1977-03-11.json"
        json_file = storage.open(f'TMDB/detail/1977-03-11/{file_name}')
    if id == '569094' :
        file_name = f"TMDB_movieDetails_{id}_2023-05-26.json"
        json_file = storage.open(f'TMDB/detail/2023-05-26/{file_name}')

    data = json_file.read()
    decoded_data = json.loads(data.decode('utf-8'))

    context = {
        'movie' : decoded_data
    }

    return render(request, 'userpage/moviedetail.html', context)
