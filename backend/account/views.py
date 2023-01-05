from django.shortcuts import render
from rest_framework import generics, permissions

from .models import Account
from .serializers import AccountSerializer

# Create your views here.

class AccountCreateApiView(generics.CreateAPIView):

    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)