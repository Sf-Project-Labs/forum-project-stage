from rest_framework.routers import DefaultRouter
from .views import StartupProfileViewSet

"""
URL configuration for the `profiles` app.

Defines the routes for accessing the `StartUpProfile` API endpoints.
"""
router = DefaultRouter()
router.register('start-up', StartupProfileViewSet, basename='startup')

urlpatterns = router.urls

