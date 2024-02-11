from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Movie
from rating.models import Rating
from .serializers import MovieSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rating.serializers import RatingSerializer
from rest_framework import status
from .permissions import IsOwnerOrReadOnly

# Create your views here.
class StandartResultPagination(PageNumberPagination):
    page_size = 100
    page_query_param= 'page'


class MovieViewSet(ModelViewSet):   
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'director', 'genre__slug']
    filterset_fields = ['director','title','release_at', 'genre']
    ordering_fields = ['release_at', 'title', 'director', 'genre__slug']
    pagination_class = StandartResultPagination

    @action(detail=True, methods=['POST', 'DELETE', 'PUT'], permission_classes=[permissions.IsAuthenticated])
    def rating(self, request, pk=None):
        movie = self.get_object()
        user = request.user
        
        if request.method == 'POST':
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            try:
                rating = Rating.objects.get(movie=movie, owner=user)
                rating.delete()
                return Response("Рейтинг удален", status=status.HTTP_204_NO_CONTENT)
            except Rating.DoesNotExist:
                return Response("Рейтинг не найден", status=status.HTTP_404_NOT_FOUND)

        elif request.method == 'PUT':
            try:
                rating = Rating.objects.get(movie=movie, owner=user)
                serializer = RatingSerializer(rating, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            except Rating.DoesNotExist:
                return Response("Рейтинг не найден", status=status.HTTP_404_NOT_FOUND)
            
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]



