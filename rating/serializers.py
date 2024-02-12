from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie = serializers.ReadOnlyField(source='movie.title')
    # rating = serializers.SerializerMethodField(method_name='validate_rating')

    # def validate_rating(self, rating):
    #     if type(rating) is str:
    #         raise serializers.ValidationError('Рейтинг должен быть числом')
    #     if not rating in range(1,6):
    #         raise serializers.ValidationError('Рейтинг должен быть в диапозаное от 1 до 5')

    class Meta:
        model = Rating
        fields = "__all__"
