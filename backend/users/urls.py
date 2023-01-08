from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("verify/", VerifyOtp.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("reset/", RequestResetView.as_view()),
    path("password/", PasswordResetView.as_view()),
    path("pin/", ResetPinView.as_view()),
]
