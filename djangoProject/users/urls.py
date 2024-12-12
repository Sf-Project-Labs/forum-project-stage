
from django.urls import path, include
from .views import LoginView, LogoutView, home, UserRegistrationView, SignInView

urlpatterns = [
    path('', home, name='home'),
    path('sign-up/', UserRegistrationView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

