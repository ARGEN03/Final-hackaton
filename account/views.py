from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .serializers import RegisterSerializer, LogOutSerializer
from .tasks import send_confirmation_email_task, send_password_reset_email_task


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
                return Response('Письмо не отправлено', status=400)
            
        return Response('Письмо отправлено', status=201)
    
class ActivationView(APIView):
    def post(self, request):
        activation_code = request.data.get('activation_code')
        if not activation_code:
            return Response('Нет кода активации', status=400)
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Активация прошла успешно', status=200)

class LogoutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response('Успешно разлогинилсь',status=200)
    
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response('Поле email не может быть пустым', status=400)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response('Пользователь не найден', status=404)
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f'/api/account/reset_password_confirm/{uid}/{token}/')
        send_password_reset_email_task.delay(email, reset_link)
        return Response('Ссылка для сброса пароля отправлена', status=200)
    
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('password')
            new_confirm_password = request.data.get('password_confirm')
            if new_password == new_confirm_password:
                user.set_password(new_password)
                user.save()
                return Response('Пароль успешно изменен', status=200)
            else:
                return Response('Пароли не совпадают', status=400)
        else:
            return Response('Неверная ссылка', status=400)

        

        


