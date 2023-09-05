from django.urls import path

from sms_site.views import dictionary

urlpatterns = [
    path('', dictionary),
]