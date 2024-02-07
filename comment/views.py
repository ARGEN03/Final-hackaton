from rest_framework.viewsets import ModelViewSet
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
