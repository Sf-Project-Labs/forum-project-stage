from django.urls import path, include
from .views import StartupRegistrationView, StartUpProfileInfo, StartUpProfileEdit

urlpatterns = (
    path('start-up/', include([
        path('create/', StartupRegistrationView.as_view(), name='startup-registration'),
        path('info/<int:id>/', StartUpProfileInfo.as_view(), name='startup-info'),
        path('edit/<int:id>/', StartUpProfileEdit.as_view(), name='startup-edit'),
    ])),
)
