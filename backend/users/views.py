from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime

from .serializers import UserSerializer, VerifyAccountSerializer, LoginSerializer, PasswordViewSerializer, PasswordResetSerializer
from .models import User

from .email import *
# Create your views here.

class RegisterView(APIView):
    """Class based view for registration"""

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            send_otp_via_email(serializer.data['email'])
            return Response({
                'status':200,
                'message':'You have been successfully registered check your email',
                'data':serializer.data
            })
        
        return Response({
            'status':400,
            'message':'something went wrong',
            'data':serializer.errors
       })

class VerifyOtp(APIView):

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors
                })

            if user[0].otp != otp:
                return Response({
                    'status':400,
                    'message':'something went wrong',
                    'data':'wrong otp'
                })

            if user[0].isVerified == True:
                return Response({
                    'status':400,
                    'message':'You are already verified',
                    'data':{}
                })

            user = user.first()

            user.isVerified = True
            user.balance = 1000.00
            user.save()

            return Response({
                'status':200,
                'message':'You have been successfully verified your email',
                'data':{}
            })



class LoginView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']

            user = authenticate(email=email, password=password)

            if user is None:
                return Response({
                    'status':400,
                    'message':'Wrong Username or Password',
                    'data':{}
                })

            if user.isVerified is False:
                return Response({
                    'status':400,
                    'message':'You have not verified your account',
                    'data':{}
                })

            user.last_login = datetime.now()
            user.save()

            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })


        return Response({
                'status':400,
                'message':'Wrong info entered',
                'data':{}
            })


class LogoutView(APIView):
    """Class base view for logout"""

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"you are logged out",
        }
        return response


class RequestResetView(APIView):
    """Class based view for reset password request."""

    def post(self, request):
        serializer = PasswordViewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]

            return Response(
                {"message":"Check email to reset your password"},
                status=200
            )

class PasswordResetView(APIView):
    """Class based view for reset password"""

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            recovery_otp = serializer.validated_data["recovery_otp"]

            user = User.objects.filter(email=email)

            if not user.exists():
                return Response(
                    {"message": "Invalid Email"},
                    status=400
                )

            if user[0].recovery_otp != recovery_otp:
                return Response(
                    {"message": "Invalid OTP"},
                    status=400
                )

            user = user.first()

            user.set_password(password)
            user.recovery_otp = None
            user.save()

            return Response(
                {"message": "Your password has been reset"},
                status=200
            )