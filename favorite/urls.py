from django.urls import path
from .views import FavoriteListCreateAPIView, FavoriteRetrieveDestroyAPIView

urlpatterns = [
    path('favorite/', FavoriteListCreateAPIView.as_view(), name='viewed-list-create'),
    path('favorite/<int:pk>/',FavoriteRetrieveDestroyAPIView.as_view(), name='viewed-retrieve-destroy'),
]