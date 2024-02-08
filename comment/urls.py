from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewSet


router = DefaultRouter()
router.register('', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    # path('comments/<int:pk>/like/', CommentViewSet.as_view({'post': 'like'}), name='comment-like')
    
]