"""
URL Configuration for the `users` app.

This module maps URL patterns to their corresponding views for user-related functionalities.

Routes:
- '' (home): Displays the home page of the application.
- 'register/' (UserRegistrationView): Handles user registration.
- 'login/' (LoginView): Manages user login.
- 'logout/' (LogoutView): Manages user logout.
"""

from django.urls import path
from .views import LoginView, LogoutView, home, UserRegistrationView

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]