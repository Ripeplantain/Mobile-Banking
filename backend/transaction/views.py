from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import TransferSerializer
from accounts.models import Account

# Create your views here.

class TransferView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            account = Account.objects.filter(phonenumber=serializer.data['receiver'])
            if not account.exists():
                return Response({
                    "message":"Account doesnot exist"
                })

            return Response({
                "message":"Hello World"
            })