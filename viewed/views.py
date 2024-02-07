from rest_framework.viewsets import ModelViewSet
from .models import Viewed
from .serializers import ViewedSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly

# Create your views here.
class ViewedViewSet(ModelViewSet):
    queryset = Viewed.objects.all()
    serializer_class = ViewedSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)