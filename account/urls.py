from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import RegistrationView, ActivationView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView, UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/<activation_code>/',ActivationView.as_view()),
    path('login/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('reset_password/',PasswordResetRequestView.as_view()),
    path('reset_password_confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view()),
    path('', include(router.urls))
]