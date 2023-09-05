from django.urls import path

from sms_site.views import *

urlpatterns = [
    # path('', dictionary),
    path('', home)
]