from rest_framework import serializers
from .models import Comment
from movie.models import Movie

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    
    class Meta:
        model = Comment
        fields = "__all__"