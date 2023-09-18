from storages.backends.s3boto3 import S3Boto3Storage
from django.shortcuts import render, redirect
import json

def userpage(request) :

    user = request.user
    is_authenticated = user.is_authenticated
    if not is_authenticated:
        return redirect('/login')

    context = {
        'user' : user
    }
    
    return render(request, 'userpage/mypage.html', context)