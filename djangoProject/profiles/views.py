from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import StartUpProfile
from .serializers import StartUpProfileSerializer


class StartUpProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for the `StartUpProfile` model.

    Provides list, create, retrieve, update, and delete actions
    for startup profiles. Supports search and filtering.

    Attributes:
        queryset (QuerySet): The set of `StartUpProfile` objects.
        serializer_class (Serializer): Serializer class for startup profiles.
        filter_backends (list): Backend classes for filtering and searching.
        search_fields (list): Fields available for search functionality.
        filterset_fields (list): Fields available for filtering.
    """
    queryset = StartUpProfile.objects.all()
    serializer_class = StartUpProfileSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['company_name', 'legal_name', 'industry_type', 'region']
    filterset_fields = ['region', 'industry_type', 'investment_needs']