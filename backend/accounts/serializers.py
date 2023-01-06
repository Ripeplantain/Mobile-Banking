from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Account
from users.models import User


class AccountSerializer(serializers.Serializer):
        phonenumber =serializers.CharField(max_length=255)
        pin = serializers.CharField(max_length=6)
        balance = serializers.DecimalField(max_digits=20,decimal_places=2)
        
        user = UserSerializer(read_only=True)
        
        def create(self, validated_data):
                return Account.objects.create(**validated_data)
