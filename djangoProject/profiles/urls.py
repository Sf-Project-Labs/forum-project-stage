"""
URL configuration for the `profiles` app.

Defines the routes for accessing the `StartUpProfile` API endpoints.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StartUpProfileViewSet

router = DefaultRouter()
router.register(r'startups', StartUpProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
