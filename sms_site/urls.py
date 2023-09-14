from django.urls import path

from sms_site.views import *

urlpatterns = [
    # path('', dictionary),
    path('', dictionary, name='dictionary')
    # path('<str:genre>/', movie_filter_by_genre, name='movie_filter_by_genre')
]