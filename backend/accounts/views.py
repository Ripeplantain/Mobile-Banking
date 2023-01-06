from rest_framework import generics, permissions

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

class AccountDetailView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'pk'
    permission_classes = (permissions.IsAuthenticated,)