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
