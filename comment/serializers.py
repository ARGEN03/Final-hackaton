from rest_framework import serializers
from .models import Comment, Like
from movie.models import Movie

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    likes = LikeSerializer(many=True, read_only=True) 

    
    class Meta:
        model = Comment
        fields = "__all__"