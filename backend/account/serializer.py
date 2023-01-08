from rest_framework import serializers

from .models import TransferHistory
from users.serializers import UserSerializer

class TransferSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    class Meta:
        model = TransferHistory
        fields = '__all__'