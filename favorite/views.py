from rest_framework.viewsets import ModelViewSet
from .models import Favorite
from .serializers import FavoriteSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly

# Create your views here.
class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


