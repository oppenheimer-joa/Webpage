# add modules - p188, p206
from django.shortcuts import render
from django.shortcuts import redirect
from storages.backends.s3boto3 import S3Boto3Storage
import json

# add index - p188
def index(request):
    # add settings - p206
    if request.user.is_authenticated:
        return redirect('/posts/main/')
    else:
        return redirect('/users/login/')
    
    # removed - p206
    # return render(request, "index.html")

# removed - p206
# add login - p197
# def login_view(request):
#     return render(request, 'users/login.html')

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

    return render(request, 'dictionary.html', {"movie_details": movie_details})