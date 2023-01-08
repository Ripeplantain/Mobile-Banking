from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/',views.UserDetailsView.as_view()),
    path('transfer/',views.TransferView.as_view()),
    path('transfer/<int:sender>/',views.TransferHistoryView.as_view()),
    path('withdraw/',views.WithdrawView.as_view()),
    path('withdraw/<int:user>/',views.WithdrawHistoryView.as_view()),
] 