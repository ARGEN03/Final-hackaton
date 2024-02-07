from rest_framework import serializers
from .models import Plan
from movie.models import Movie

class PlanSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Plan
        fields = "__all__"