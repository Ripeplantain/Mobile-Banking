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
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                receiver = User.objects.select_for_update().filter(phonenumber=serializer.data['receiver'])
                sender = User.objects.select_for_update().filter(id=request.user.id).first()
                if receiver.exists():
                    receiver = receiver.get()
                    if sender.pin == request.data['pin']:
                        if float(serializer.data['amount']) < sender.balance:
                                receiver.balance += Decimal(serializer.data['amount'])
                                receiver.save()

                                sender.balance -= Decimal(serializer.data['amount'])
                                sender.save()

                                return Response(status=200)
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