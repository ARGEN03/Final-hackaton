from rest_framework.viewsets import ModelViewSet
from .models import Genre
from .serializers import GenreSerializer
from rest_framework import permissions

# Create your views here.
class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]

