from rest_framework import serializers
from .models import Viewed
from movie.models import Movie

class ViewedSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Viewed
        fields = "__all__"