# 이미지 업로드 용 필드 추가
# 생성 후 migration 진행

from django.db import models

class ExternalImageModel(models.Model):
    image_url = models.CharField(max_length=255)
