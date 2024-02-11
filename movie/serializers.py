from rest_framework import serializers
from .models import Movie
from genre.models import Genre
from genre.serializers import GenreSerializer
from rating.serializers import RatingSerializer
from comment.serializers import CommentSerializer
from django.db.models import Avg
from plan.models import Plan
from viewed.models import Viewed
from favorite.models import Favorite


class MovieSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())  # Используем HiddenField для автоматической установки owner_id
    genre = serializers.SerializerMethodField(method_name='get_genre')
    comments = serializers.SerializerMethodField(method_name='get_comments')
    favorite = serializers.SerializerMethodField(method_name='get_favorite')
    planned = serializers.SerializerMethodField(method_name='get_planned')
    watched = serializers.SerializerMethodField(method_name='get_watched')
    

    def get_planned(self, obj):
        try:
            if Plan.objects.filter(movie=obj).exists():
                return "Planned"
            else:
                return "Empty"
            
        except Exception as e:
            return "Ошибка: {}".format(str(e))
    
    def get_watched(self, obj):
        try:
            if Viewed.objects.filter(movie=obj).exists():
                return "Watched"
            else:
                return "Empty"
            
        except Exception as e:
            return "Ошибка: {}".format(str(e))
        
    def get_favorite(self, obj):
        try:
            if Favorite.objects.filter(movie=obj).exists():
                return "My favorite"
            else:
                return "Empty"
            
        except Exception as e:
            return "Ошибка: {}".format(str(e))

        

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
        fields = ['id', 'title', 'owner_email', 'owner', 'genre', 'comments','content', 'image', 'video','planned', 'watched', 'favorite']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['rating'] = instance.ratings.aggregate(
            Avg('rating')
        )
        rating = rep['rating']
        rating['rating_count'] = instance.ratings.count()
        return rep


