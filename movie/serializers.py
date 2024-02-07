from rest_framework import serializers
from .models import Movie
from genre.models import Genre
from django.db.models import Avg


class MovieSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Используем HiddenField для автоматической установки owner_id
    genre = serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all()) 

    class Meta:
        model = Movie
        fields = '__all__'