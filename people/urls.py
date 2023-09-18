from django.urls import path

from people.views import *


urlpatterns = [
    path('people/', dictionary, name='dictionary'),
    path('people/<str:id>/', people_info, name='people_info')
]