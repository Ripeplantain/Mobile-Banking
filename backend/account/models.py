from django.db import models

from users.models import User

# Create your models here.

class TransferHistory(models.Model):
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    receiver = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"


class WithdrawHistory(models.Model):
    amount = models.DecimalField(max_digits=15,decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"