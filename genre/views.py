from rest_framework.viewsets import ModelViewSet
from .models import Genre
from .serializers import GenreSerializer
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# # Create your views here.
class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['title']

    # @method_decorator(cache_page(60*15))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    
