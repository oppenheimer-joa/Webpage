from django.urls import path

from sms_site.views import *

urlpatterns = [
    # path('', dictionary),
    path('', home),
    path('genre/', genre_list),
    path('movie/', dictionary, name='dictionary'),
    path('movie/<str:genre>/', movie_filter_by_genre, name='moviegenre')
]