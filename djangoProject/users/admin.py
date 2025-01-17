"""
Admin configuration for the `User` model.

This module defines how the `User` model is displayed and managed
in the Django admin interface.
"""

from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for the `User` model.

    This class customizes the display of `User` model instances
    in the Django admin panel.

    Attributes:
        list_display (tuple): Fields to display in the admin list view.
        search_fields (tuple): Fields to enable search functionality.
        list_filter (tuple): Fields to filter the user list in the admin panel.
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
