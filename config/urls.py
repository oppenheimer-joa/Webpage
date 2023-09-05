from django.contrib import admin
from django.urls import path, include # p199

# add modules - p188
from django.conf import settings
from django.conf.urls.static import static
from config.views import index

urlpatterns = [
    path('userpage/', include('userpage.urls')),
    path('dict/', include('sms_site.urls')),
    path('admin/', admin.site.urls),
    # add path - p202
    path('posts/', include('posts.urls')),
    # add path - p199
    path('users/', include('users.urls')),
    # add path - p188
    path('', index)
]

# add urlpatterns - p188
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
