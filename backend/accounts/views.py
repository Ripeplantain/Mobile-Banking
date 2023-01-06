from rest_framework import generics, permissions
# from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import AccountSerializer
from .models import Account
from users.models import User



# Create your views here.

class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        user = User.objects.get(pk=self.request.user.id)
        serializer.save(user=user)

class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer