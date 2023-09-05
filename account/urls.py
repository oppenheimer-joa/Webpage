from django import *
from django.urls import re_path
# from django.conf.urls import url
from django.conf.urls import include
from . import views

app_name = 'account'
urlpatterns = [
    re_path('', views.login, name='login')
]