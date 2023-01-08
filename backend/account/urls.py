from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/',views.UserDetailsView.as_view()),
    path('transfer/',views.TransferView.as_view()),
] 