from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie = serializers.ReadOnlyField(source='movie.title')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Рейтинг должен быть в диапазоне от 1 до 5.')
        return value

    class Meta:
        model = Rating
        fields = "__all__"
