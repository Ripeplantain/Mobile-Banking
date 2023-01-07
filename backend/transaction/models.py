from django.db import models

from users.models import User
from accounts.models import Account

# Create your models here.

class TransferHistory(models.Model):
    amount =models.DecimalField(max_digits=15,decimal_places=2)
    receiver = models.CharField(max_length=255)
    sender = models.OneToOneField(User,on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.receiver} has received {self.amount}"