from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Favorite
from .serializers import FavoriteSerializer
# from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from rest_framework import permissions
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from movie.models import Movie
from django.core.exceptions import ObjectDoesNotExist

class FavoriteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__title'] 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def create(self, request, *args, **kwargs):

        movie_id = request.data.get('movie', None)
        if movie_id is None:
            return Response({"movie": "ID фильма не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Movie.objects.get(id=movie_id)
        except ObjectDoesNotExist:
            return Response({"movie": "Фильм с указанным ID не существует"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"movie": "Такой фильм уже существует"}, status=status.HTTP_400_BAD_REQUEST)

class FavoriteRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]