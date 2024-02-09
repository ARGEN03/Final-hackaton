from rest_framework import serializers
from .models import Genre



class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"

#     def get_children(self, obj):
#         children = obj.children.all()
#         return [{'name': child.name} for child in children]