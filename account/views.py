from http import HTTPStatus

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions

from .serializers import RegisterSerializer, LogOutSerializer
from .tasks import send_confirmation_email_task

User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = serializers.save()
        if user:
            try:
                send_confirmation_email_task.delay(user.email, user.activation_code)
            except:
                return Response('Письмо не отправлено', status=HTTPStatus.BAD_REQUEST)
            
        return Response('Письмо отправлено', status=HTTPStatus.CREATED)
    
class ActivationView(APIView):
    def post(self, request):
        activation_code = request.data.get('activation_code')
        if not activation_code:
            return Response('Нет кода активации', status=HTTPStatus.BAD_REQUEST)
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Активация прошла успешно', status=HTTPStatus.OK)

class LogoutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно разлогинилсь', 200)


