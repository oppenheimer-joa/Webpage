from django.contrib import admin
from django.urls import path, include # p199

# add modules - p188
from django.conf import settings
from django.conf.urls.static import static
from config.views import index
from sms_site.views import *

urlpatterns = [
    # default page
    # path('', include('sms_site.urls')),       ## 나중에 시작 페이지랑 연결
    # login & account
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    # main page
    path('main/', include('posts.urls')),    ## 나중에 메인 페이지랑 연결  include
    # movie info
    path('movie/', include('sms_site.urls')),
    # performance info
    ## path('performance/', include('performance.urls')),
    # user info
    path('userinfo/', include('userpage.urls')),
    path('performance/', performance),
    path('', include('people.urls')),
    path('', include('award.urls'))

    
    
]

# add urlpatterns - p188
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
