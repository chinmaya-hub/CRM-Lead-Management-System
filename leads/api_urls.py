from django.urls import path
from . import api_views

urlpatterns = [
    path('leads/', api_views.LeadListCreateAPIView.as_view(), name='api-leads'),
    path('leads/<int:pk>/', api_views.LeadDetailAPIView.as_view(), name='api-lead-detail'),
]