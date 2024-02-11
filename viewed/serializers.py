from rest_framework import serializers
from .models import Viewed
from movie.models import Movie

class ViewedSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie_title = serializers.SerializerMethodField(method_name='get_movie_title')

    def get_movie_title(self, obj):
        return obj.movie.title if obj.movie else None
    

    class Meta:
        model = Viewed
        fields = ['id','owner', 'created_at', 'movie', 'movie_title']