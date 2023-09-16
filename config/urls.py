from django.contrib import admin
from django.urls import path, include # p199

# add modules - p188
from django.conf import settings
from django.conf.urls.static import static
from config.views import index
from sms_site.views import *

urlpatterns = [
    path('', include('users.urls')),
    # main page
    path('', include('posts.urls')), 
    # movie info
    path('', include('sms_site.urls')),

    path('', include('userpage.urls')),
    path('admin/', admin.site.urls),

    # path('', performance),
    path('', include('people.urls')),
    path('', include('award.urls')),
]

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
