from django.urls import path
from .views import ViewedListCreateAPIView, ViewedRetrieveDestroyAPIView

urlpatterns = [
    path('view/', ViewedListCreateAPIView.as_view(), name='viewed-list-create'),
    path('view/<int:pk>/',ViewedRetrieveDestroyAPIView.as_view(), name='viewed-retrieve-destroy'),
]