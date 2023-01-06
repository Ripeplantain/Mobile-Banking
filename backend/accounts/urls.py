from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.AccountCreateView.as_view()),
    path('<int:pk>/', views.AccountDetailView.as_view()),
]