from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(max_length=255,unique=True)
    isVerified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True)
    phone_number = models.CharField(max_length=255,unique=True,null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

