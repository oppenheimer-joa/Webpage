# add modules - p201
from django.urls import path
from posts.views import main

# add urlpatterns - p201
urlpatterns = [
    path('', main),
]