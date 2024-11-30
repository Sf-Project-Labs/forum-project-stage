from django.shortcuts import render


from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .models import User

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
