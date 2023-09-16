# add modules - p201
from django.urls import path
from posts.views import *

from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('main/', views.main, name='main'),

    path('dir/', views.directory, name='dir'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),

    path('about/', views.about, name='about'),
    path('about/outline/', views.outline, name='outline'),
    path('about/team/', views.team, name='team'),
    path('about/release/', views.release, name='release'),
    path('about/api/', views.api, name='api'),

    path('help/', views.help, name='help'),
    path('help/faq/', views.faq, name='faq'),
    path('help/qna/', views.qna, name='qna'),
    path('help/inq/', views.inq, name='inq'),

    path('document/', views.document, name='document'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)