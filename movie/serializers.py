from rest_framework import serializers
from .models import Movie
from genre.models import Genre
from comment.serializers import CommentSerializer


class MovieSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Используем HiddenField для автоматической установки owner_id
    genre = serializers.PrimaryKeyRelatedField(required=True, queryset=Genre.objects.all()) 
    comments = serializers.SerializerMethodField(method_name='get_comments')

    def get_comments(self, instance):
        comments = instance.comments.all()
        serializer = CommentSerializer(
            comments, many=True
        )
        return serializer.data

    class Meta:
        model = Movie
        fields = '__all__'