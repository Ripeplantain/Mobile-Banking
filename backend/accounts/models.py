from django.db import models

from users.models import User

# Create your models here.

class Account(models.Model):
    phonenumber = models.CharField(max_length=255,unique=True)
    balance = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    pin = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phonenumber