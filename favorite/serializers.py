from django.db import IntegrityError
from rest_framework import serializers
from .models import Favorite
from movie.models import Movie
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie_title = serializers.SerializerMethodField(method_name='get_movie_title')

    
    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None

    class Meta:
        model = Favorite
        fields = ['id', 'owner', 'movie','created_at','movie_title']

