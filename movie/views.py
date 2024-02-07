from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Movie
from .serializers import MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class StandartResultPagination(PageNumberPagination):
    page_size = 100
    page_query_param= 'page'


class MovieViewSet(ModelViewSet):   
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'director', 'genre']
    filterset_fields = ['genre']
    pagination_class = StandartResultPagination


    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAdminUser()]