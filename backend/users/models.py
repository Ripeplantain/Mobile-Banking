from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.CharField(max_length=255,unique=True)
    pin = models.IntegerField()
    phone_number = models.CharField(max_length=255,unique=True,null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []