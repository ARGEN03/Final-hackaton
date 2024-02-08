from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Like
from .serializers import CommentSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly
from rest_framework import permissions

# Create your views here.

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        comment = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, comment=comment)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        serializer = self.get_serializer(comment)
        return Response({'liked': liked, 'comment': serializer.data})

    def perform_create(self, serializer):
        # comment = serializer.save(owner=self.request.user)
        serializer.save(owner=self.request.user)
