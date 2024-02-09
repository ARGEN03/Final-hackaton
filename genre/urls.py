from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet


router = DefaultRouter()
router.register('', GenreViewSet)

urlpatterns = [
    path('', include(router.urls))
]
