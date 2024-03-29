from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render
import uuid

from .serializers import RegisterSerializer, LogOutSerializer, UserSerializer
from .tasks import send_confirmation_email_task, send_password_reset_email_task
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class RegistrationView(APIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.activation_code = uuid.uuid4()
            user.save()

            activation_path = f'/api/account/activate/{user.activation_code}/'
            activation_url = request.build_absolute_uri(activation_path)
            
            try:
                send_confirmation_email_task.delay(user.email, activation_url)
                return Response('Письмо с активацией отправлено', status=201)
            except:
                return Response('Ошибка отправки письма', status=400)
        else:
            return Response(serializer.errors, status=400)
        
class ActivationView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            context = {'message': 'Account activated successfully'}
            return render(request, 'activation_success.html', context)
            # return Response({'message': 'Account activated successfully'})
        except User.DoesNotExist:
            context = {'error': 'Invalid or expired token'}
            return render(request, 'activation_error.html', context, status=404)
            # return Response({'error': 'Invalid or expired token'}, status=404)
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

    @swagger_auto_schema(
        operation_summary="Запрос на сброс пароля",
        operation_description="Отправляет пользователю ссылку для сброса пароля на указанный email.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description="Email пользователя, который запрашивает сброс пароля.")
            },
            required=['email']
        ),
        responses={
            200: openapi.Response(description="Ссылка для сброса пароля отправлена на указанный email."),
            400: openapi.Response(description="Поле email не может быть пустым или другая ошибка в запросе."),
            404: openapi.Response(description="Пользователь не найден.")
        }
    )
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsOwnerOrReadOnly()]
        
        
        


