
from django.urls import path, include
from .views import LoginView, home, UserRegistrationView

urlpatterns = [
    path('', home, name='home'),
    path('sign-up/', UserRegistrationView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),
]