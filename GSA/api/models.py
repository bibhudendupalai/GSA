from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomeUser(AbstractUser):
    is_verify = models.BooleanField(default=False)
    fullname=models.CharField(max_length=100)
    password2=models.CharField(max_length=100)

    REQUIRED_FIELDS = ['email', 'is_verify']

class TodoList(models.Model):
    user=models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)

