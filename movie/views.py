from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Movie
from .serializers import MovieSerializer

# Create your views here.
class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]