from rest_framework import serializers
from .models import Favorite
from movie.models import Movie

class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie_title = serializers.SerializerMethodField(method_name='get_movie_title')

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None

    class Meta:
        model = Favorite
        fields = ['owner', 'created_at', 'movie', 'movie_title']

