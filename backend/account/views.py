from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import IntegrityError, transaction

from users.serializers import UserSerializer
from .serializer import TransferSerializer
from users.models import User

from decimal import Decimal

# Create your views here.
class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'


class TransferView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        request.data['sender'] = self.request.user.id

        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                receiver = User.objects.select_for_update().filter(phonenumber=serializer.validated_data.get('receiver'))
                sender = User.objects.select_for_update().filter(id=request.user.id).first()
                if receiver.exists():
                    receiver = receiver.get()
                    if sender.pin == request.data['pin']:
                        if float(serializer.validated_data.get('amount')) < sender.balance:
                                receiver.balance += Decimal(serializer.validated_data.get('amount'))
                                receiver.save()

                                sender.balance -= Decimal(serializer.validated_data.get('amount'))
                                sender.save()
                                
                                serializer.save()
                                return Response(serializer.data, status=200)    
                        else:
                            return Response(
                                status=400,
                                data={'message': 'Insufficient balance.'}
                            )
                    else:
                        return Response({
                            "error":"Wrong pin"
                        },status=403)
                else:
                    return Response({
                        "error": "Receiver does not exist"
                    })