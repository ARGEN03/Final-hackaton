from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Viewed
from .serializers import ViewedSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from plan.models import Plan

class ViewedListCreateAPIView(generics.ListCreateAPIView):
    queryset = Viewed.objects.all()
    serializer_class = ViewedSerializer
    # permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['movie__title'] 

    def perform_create(self, serializer):
        owner = self.request.user
        if isinstance(owner, AnonymousUser):
            raise IntegrityError("Пользователь должен быть аутентифицирован для создания записи")
        serializer.save(owner=owner)

    def create(self, request, *args, **kwargs):
        movie_title = request.data.get('movie_title')
        try:
            # Проверяем, существует ли фильм в списке Plan
            plan_movie = Plan.objects.filter(movie__title=movie_title, owner=request.user)
            # Если фильм найден в списке Plan, удаляем его
            plan_movie.delete()
        except Plan.DoesNotExist:
            pass  # Фильм не найден в списке Plan или пользователь не является владельцем, ничего не делаем
        return super().create(request, *args, **kwargs)

class ViewedRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Viewed.objects.all()
    serializer_class = ViewedSerializer
    # permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]
    permission_classes = [permissions.IsAuthenticated]
