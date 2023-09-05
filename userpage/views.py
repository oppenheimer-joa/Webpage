from storages.backends.s3boto3 import S3Boto3Storage
from django.shortcuts import render
import json

# Create your views here.
def userdetail(request) :
    context = {}
    user_info = request.session['login_session']

    context = {
        'user_nm': user_info
    }
    return render(request, 'userpage/userdetail.html', context)

def moviedetail(request) :
    storage = S3Boto3Storage()
    idx = '872585'
    file_name = f"TMDB_movieDetails_{idx}_2023-07-14.json"
    json_file = storage.open(f'TMDB/detail/2023-07-14/{file_name}')
    print(json_file)
    data = json_file.read()
    decoded_data = json.loads(data.decode('utf-8'))

    context = {
        'original_title' : decoded_data["original_title"],
        'poster_path' : decoded_data["poster_path"]
    }

    return render(request, 'userpage/moviedetail.html', context)
