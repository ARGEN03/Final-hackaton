from rest_framework import serializers
from .models import Movie
from genre.models import Genre
from genre.serializers import GenreSerializer
from rating.serializers import RatingSerializer
from comment.serializers import CommentSerializer
from django.db.models import Avg
from plan.models import Plan
from viewed.models import Viewed


class MovieSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Используем HiddenField для автоматической установки owner_id
    genre = serializers.SerializerMethodField(method_name='get_genre')
    comments = serializers.SerializerMethodField(method_name='get_comments')
    planned = serializers.SerializerMethodField(method_name='get_planned')
    watched = serializers.SerializerMethodField(method_name='get_watched')

    # def get_watched(self, obj):
    #     owner = self.context['request'].user
    #     try:
    #         Viewed.objects.filter(movie=obj).exists()
    #         return 'Просмотрен'
    #     except:
    #         return 'Нет'

    # def get_planned(self, obj):
    #     owner = self.context['request'].user
    #     try:
    #         Plan.objects.filter(movie=obj).exists()
    #         return 'Запланирован'
    #     except:
    #         return 'Нет'

    def get_planned(self, obj):
        # user = self.context['request'].user
        return Plan.objects.filter(movie=obj).exists()
    
    def get_watched(self, obj):
        # user = self.context['request'].user
        return Viewed.objects.filter(movie=obj).exists()

    def get_genre(self, obj):
        return obj.genre.slug if obj.genre else None

    def get_comments(self, instance):
        comments = instance.comments.all()
        serializer = CommentSerializer(
            comments, many=True
        )
        return serializer.data
    
        

    class Meta:
        model = Movie
        fields = ['id', 'title', 'owner_email', 'owner', 'genre', 'comments','content', 'image', 'video','planned', 'watched']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.ratings.aggregate(
            Avg('rating')
        )
        rating = rep['rating']
        rating['rating_count'] = instance.ratings.count()
        return rep


