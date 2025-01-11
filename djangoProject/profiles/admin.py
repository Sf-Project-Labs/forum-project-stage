"""
Admin configuration for the `profiles` app.

This module defines how the `StartUpProfile` model is displayed and managed
in the Django admin interface.
"""

from django.contrib import admin
from .models import StartUpProfile


@admin.register(StartUpProfile)
class StartUpAdmin(admin.ModelAdmin):
    """
    Admin configuration for the `StartUpProfile` model.

    This class customizes the display, search, and filtering capabilities
    for startup profiles in the Django admin panel.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields available for search functionality.
    """
    list_display = ('company_name', 'legal_name', 'email', 'phone_number', 'region',
                    'industry_type', 'user', 'project_information', 'company_size', 'investment_needs')
    search_fields = ('company_name', 'legal_name')