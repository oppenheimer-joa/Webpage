from django.db import models

# Create your models here.
class moviedata(models.Model):
    name = models.CharField(max_length=100)  
    s3_file_path = models.CharField(max_length=255)  # S3 파일 
    

    def __str__(self):
        return self.name