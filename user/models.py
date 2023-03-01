from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    city = models.CharField(max_length=100,null=True)
    phnno = models.IntegerField(null=True)

class UserLog(models.Model):
    method=models.CharField(max_length=150)
    url=models.CharField(max_length=250)
    count=models.IntegerField(default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)



