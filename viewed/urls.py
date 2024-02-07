from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ViewedViewSet


router = DefaultRouter()
router.register('', ViewedViewSet)

urlpatterns = [
    path('', include(router.urls))
]