# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from .serializers import UserSerializer, VerifyAccountSerializer
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

                user[0].isVerified = True
                user[0].save()

                return Response({
                    'status':200,
                    'message':'You have been successfully verified your email',
                    'data':{}
                })

        except Exception as e:
            print(e)

class LoginView(APIView):
    """Class based view for login"""

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email)

        if user[0].isVerified == False:
            raise AssertionError('Verify your email')

        user = user.first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid password')

        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token,
        }
        return response

class LogoutView(APIView):
    """Class base view for logout"""

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message":"you are logged out",
        }
        return response