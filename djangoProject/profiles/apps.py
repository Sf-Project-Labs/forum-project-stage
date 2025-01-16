"""
App configuration for the `profiles` app.

This module defines the configuration class for the `profiles` app,
specifying app-specific settings.
"""

from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """
    Configuration class for the `profiles` application.

    Attributes:
        default_auto_field (str): Specifies the type of auto-generated field for primary keys.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'