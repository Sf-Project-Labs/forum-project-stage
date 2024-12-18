from django.urls import path
from .views import LoginView, LogoutView, home, UserRegistrationView, health_check

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('health/', health_check, name='health'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

