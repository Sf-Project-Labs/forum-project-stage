from django.urls import path
from .views import LoginView, LogoutView, home, UserRegistrationView

urlpatterns = [
    path('', home, name='home'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
