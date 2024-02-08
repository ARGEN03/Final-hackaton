from rest_framework import serializers
from .models import Plan
from movie.models import Movie

class PlanSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    movie__title = serializers.CharField(source='movie.title')
    class Meta:
        model = Plan
        fields = ['owner', 'created_at', 'movie', 'movie__title']