from django.contrib import admin
from .models import UserInfo
# Register your models here.
@admin.register(UserInfo)

class UserAdmin(admin.ModelAdmin) :
    list_display = (
        'user_id',
        'user_pw',
        'user_nm',
        'user_email',
        'user_register_dt'
    )