from django import *
from django.urls import path
# from django.conf.urls import url
from django.conf.urls import include
from . import views

urlpatterns = [
    path('userpage', views.userdetail, name='userdetail'),
    # path('movie', views.moviedetail, name='moviedetail')
]