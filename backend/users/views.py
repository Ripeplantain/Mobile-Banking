from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

import jwt, datetime

from .serializers import UserSerializer, VerifyAccountSerializer, LoginSerializer
from .models import User

from .email import *
# Create your views here.

class RegisterView(APIView):
    """Class based view for registration"""

    def post(self, request):
        try:
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

        except Exception as e:
            print(e)

class VerifyOtp(APIView):

    def post(self, request):
        try:
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
                user.save()

                return Response({
                    'status':200,
                    'message':'You have been successfully verified your email',
                    'data':{}
                })

        except Exception as e:
            print(e)


class LoginView(APIView):
    
    def post(self, request):
        try:
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


                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({
                    'status':400,
                    'message':'You are already verified',
                    'data':{}
                })

        except Exception as e:
            print(e)

class LogoutView(APIView):
    """Class base view for logout"""

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"you are logged out",
        }
        return response