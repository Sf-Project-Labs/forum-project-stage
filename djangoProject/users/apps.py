"""
App configuration for the `users` application.

This module defines the configuration class for the `users` app,
specifying app-specific settings.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the `users` application.

    Attributes:
        default_auto_field (str): Specifies the type of auto field for models.
        name (str): The name of the application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
