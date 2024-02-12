from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie = serializers.ReadOnlyField(source='movie.title')
    rating = serializers.IntegerField(error_messages={'invalid':"Рейтинг должен быть числом"})

    def validate_rating(self, rating):
        if not rating in range(1,6):
            raise serializers.ValidationError('Рейтинг должен быть в диапозаное от 1 до 5')
        return rating

    class Meta:
        model = Rating
        fields = "__all__"
