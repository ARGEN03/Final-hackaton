from django.urls import path
from .views import PlanListCreateAPIView, PlanRetrieveDestroyAPIView

urlpatterns = [
    path('plan/', PlanListCreateAPIView.as_view(), name='viewed-list-create'),
    path('plan/<int:pk>/',PlanRetrieveDestroyAPIView.as_view(), name='viewed-retrieve-destroy'),
]