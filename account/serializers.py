from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 8, write_only = True, required = True)
    password_confirm = serializers.CharField(min_length = 8, write_only = True, required = True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required = True, write_only = True)