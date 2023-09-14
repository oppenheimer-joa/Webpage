# add modules - p201
from django.urls import path
from posts.views import *

from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

# add urlpatterns - p201
urlpatterns = [
    path('', main),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:pk>/', views.movies_detail, name='movies_detail'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
