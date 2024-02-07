from rest_framework import serializers
from .models import Genre



class GenreSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = ['id','name', 'children', 'slug', 'parent']

    def get_children(self, obj):
        children = obj.children.all()
        return [{'name': child.name} for child in children]