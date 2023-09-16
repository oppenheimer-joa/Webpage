# add modules - p201
from django.urls import path
from award.views import *

from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

# add urlpatterns - p201
urlpatterns = [
    path('awards/', views.award_list, name='award_list'),
    path('awards/<str:festa_name>/<int:year>/', views.award_detail, name='award_detail'),
]