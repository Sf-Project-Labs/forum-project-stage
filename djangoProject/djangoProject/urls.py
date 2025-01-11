"""
Main URL configuration for the Django project.

This module defines the root URL patterns for the application,
including routes for the admin panel, user-related endpoints,
profile-related endpoints, and a health check endpoint.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """
    Endpoint for checking the health of the application.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        JsonResponse: A response with a JSON object indicating the application's status.
    """
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('health/', health_check, name='health-check'),
    path('', include('profiles.urls')),
]
