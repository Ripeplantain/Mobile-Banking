from rest_framework import serializers

from .models import TransferHistory, WithdrawHistory
from users.serializers import UserSerializer

class TransferSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    class Meta:
        model = TransferHistory
        fields = '__all__'


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['sender_id'] = user.id
        return TransferHistory.objects.create(**validated_data)


class WithdrawSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    class Meta:
        model = WithdrawHistory
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return WithdrawHistory.objects.create(**validated_data)