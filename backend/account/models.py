from django.db import models

from users.models import User

# Create your models here.

class Account(models.Model):
    phonenumber = models.CharField(max_length=255,unique=True)
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    pin = models.CharField(max_length=4,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phonenumber