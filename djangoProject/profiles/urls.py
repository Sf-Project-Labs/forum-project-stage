from django.urls import path, include
from .views import StartupRegistrationView

urlpatterns = (
    path('start-up/', include([
        path('create/', StartupRegistrationView.as_view(), name='startup-registration'),
    ]))
)
