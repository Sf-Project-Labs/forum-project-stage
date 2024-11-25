from django.urls import path
from users.views import  SignUpUserView

urlpatterns = (
    path('sign-up', SignUpUserView.asView(), name='sign-up user')
)