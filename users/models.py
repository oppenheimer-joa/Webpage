from django.db import models

# import modules - p194
from django.contrib.auth.models import AbstractUser

# create user class
# 수정 시 migration 필요
class User(AbstractUser):
    profile_image = models.ImageField(
        '프로필 이미지', upload_to='users/profile', blank=True)
    short_description = models.TextField('소개글', blank=True)
