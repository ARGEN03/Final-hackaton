from rest_framework.viewsets import ModelViewSet
from .models import Plan
from .serializers import PlanSerializer
from .permissions import IsOwnerAndAuthenticatedOrReadOnly

# Create your views here.
class PlanViewSet(ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsOwnerAndAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)