from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    user_pw = models.CharField(max_length=100, blank=True, null=True)
    user_nm = models.CharField(max_length=20, blank=True, null=True)
    user_email = models.CharField(max_length=100, blank=True, null=True)
    user_register_dt = models.DateField(blank=True, null=True)

    def __str__(self) :
        return self.user_nm

    class Meta:
        managed = False
        db_table = 'user_info'
        verbose_name = '유저'
        verbose_name_plural = '유저'