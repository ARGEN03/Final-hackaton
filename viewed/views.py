from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Viewed
from .serializers import ViewedSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from django.db import IntegrityError, transaction
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from plan.models import Plan
from movie.models import Movie
from django.core.exceptions import ObjectDoesNotExist


class ViewedListCreateAPIView(generics.ListCreateAPIView):
    queryset = Viewed.objects.all()
    serializer_class = ViewedSerializer
    # permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]
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
            movie_id = request.data.get('movie')
            with transaction.atomic():
                # Проверяем, существует ли фильм уже в модели Plan
                plan_movie = Plan.objects.filter(movie=movie_id).first()
                if plan_movie:
                    plan_movie.delete()
                    # Добавляем фильм в модель Viewed
                    serializer = self.get_serializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    self.perform_create(serializer)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return super().create(request, *args, **kwargs)
                
        except IntegrityError:
            return Response({"detail": "Такой фильм уже существует"}, status=status.HTTP_400_BAD_REQUEST)

class ViewedRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Viewed.objects.all()
    serializer_class = ViewedSerializer
    permission_classes = [permissions.IsAuthenticated]
