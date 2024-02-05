from django.urls import path
from .views import RegistrationView, ActivationView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/',ActivationView.as_view()),
    path('login/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('reset_password/',PasswordResetRequestView.as_view()),
    path('reset_password_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view())
]