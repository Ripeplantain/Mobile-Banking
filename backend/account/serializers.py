from rest_framework import serializers

from .models import Account

class AccountSerializer(serializers.Serializer):
    model = Account
    fields = '__all__'

    # def create(self, validated_data):
    #     pin = validated_data.pop('pin', None)
    #     instance = self.Meta.model(**validated_data)
    #     if pin is not None:
    #         instance.set_password(pin)
    #     instance.save()
    #     return instance
