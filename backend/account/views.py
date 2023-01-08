from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from users.models import User

# Create your views here.
class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'