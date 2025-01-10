from rest_framework.routers import DefaultRouter
from .views import StartupProfileViewSet

router = DefaultRouter()
router.register('start-up', StartupProfileViewSet, basename='startup')

urlpatterns = router.urls
