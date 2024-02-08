from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from django.db import IntegrityError
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class PlanListCreateAPIView(generics.ListCreateAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['movie__title']
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

class PlanRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]