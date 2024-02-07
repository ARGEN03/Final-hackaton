from rest_framework import serializers
from .models import Favorite
from movie.models import Movie

class FavoriteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Favorite
        fields = "__all__"