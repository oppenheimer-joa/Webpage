# import module - p198, p216, p220
from django.urls import path
from users.views import login_view, logout_view, signup

# add urlpatterns
urlpatterns = [
    path('login/', login_view),
    # add path - p215
    path('logout/', logout_view),
    # add path - p220
    path('signup/', signup),
]