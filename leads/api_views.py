from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Lead
from .serializers import LeadSerializer


class LeadListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all leads.
    POST: Create a new lead.
    Supports filtering and searching.
    """

    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['status', 'source', 'assigned_to']
    search_fields = ['name', 'email', 'company', 'phone']
    ordering_fields = ['created_at', 'name', 'score']


class LeadDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve one lead.
    PUT/PATCH: Update a lead.
    DELETE: Delete a lead.
    """

    queryset = Lead.objects.all()
    serializer_class = LeadSerializer