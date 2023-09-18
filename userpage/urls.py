from django import *
from django.urls import path
# from django.conf.urls import url
from django.conf.urls import include
from userpage import views

urlpatterns = [
    path('', views.userpage, name='userdetail'),
    # path('moviedetail/<str:id>/', views.moviedetail, name='moviedetail')
]