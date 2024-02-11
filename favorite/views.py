from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from movie.models import Movie

class FavoriteListCreateAPIView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__title'] 



    def perform_create(self, serializer):
        owner = self.request.user
        if isinstance(owner, AnonymousUser):
            raise IntegrityError("Пользователь должен быть аутентифицирован для создания записи")
        serializer.save(owner=owner)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({"detail": "Такой фильм уже существует"}, status=status.HTTP_400_BAD_REQUEST)

class FavoriteRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]