from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import Http404

from users.serializers import UserSerializer
from .serializer import TransferSerializer, WithdrawSerializer
from .models import TransferHistory
from users.models import User

from decimal import Decimal


class UserDetailsView(APIView):
    """
    This view is used to show user account details
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        history = self.get_object(pk)
        serializer = UserSerializer(history)
        return Response(serializer.data)


class TransferView(APIView):
    """
        This view is used for transferring money from one user to another.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):

        # request.data['sender_id'] = self.request.user.id

        serializer = TransferSerializer(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):

            with transaction.atomic():
                receiver = User.objects.select_for_update().filter(phonenumber=serializer.validated_data.get('receiver'))
                sender = User.objects.select_for_update().filter(id=request.user.id).first()
                if receiver.exists():
                    receiver = receiver.get()
                    if sender.pin == request.data['pin']:
                        if Decimal(serializer.validated_data.get('amount')) < sender.balance:
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


class TransferHistoryView(APIView):
    """
    This view is used to show transfer history of user
    """

    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return TransferHistory.objects.get(pk=pk)
        except TransferHistory.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        history = self.get_object(pk)
        serializer = TransferSerializer(history)
        return Response(serializer.data)


class WithdrawView(APIView):
    """
    This view is used to withdraw money from account
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # request.data['user'] = self.request.user.id

        serializer = WithdrawSerializer(data=request.data,context={'request': request})
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                user = User.objects.select_for_update().filter(id=request.user.id).first()
                
                if user.pin != request.data['pin']:
                    return Response({
                        "error": "Wrong pin"
                    },status=403)

                if serializer._validated_data.get('amount') > user.balance:
                    return  Response(
                        status=400,
                        data={'message': 'Insufficient balance.'}
                    )
                else:
                    user.balance -= Decimal(serializer._validated_data.get('amount'))
                    user.save()

                    serializer.save()
                    return Response(
                        serializer.data,
                        status=200
                    )
