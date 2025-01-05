from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .serializers import StartUpProfileSerializer, InvestorProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import StartUpProfile

User = get_user_model()


class InvestorRegistrationView(CreateAPIView):
    serializer_class = InvestorProfileSerializer
    permission_classes = [AllowAny]


class StartupRegistrationView(CreateAPIView):
    serializer_class = StartUpProfileSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Extract id_user from query parameters
        id_user = self.request.query_params.get('id_user')
        if not id_user:
            raise ValidationError("User ID is missing in the query parameters.")

        # Get the User instance based on the id_user
        user = get_object_or_404(User, user_id=id_user)

        # Save the StartupProfile with the associated user
        serializer.save(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request_user_id'] = self.request.query_params.get('id_user')
        return context


class StartUpProfileInfo(RetrieveAPIView):
    queryset = StartUpProfile.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StartUpProfileSerializer
    lookup_field = 'id'

    def get_object(self):
        profile = super().get_object()
        return profile


class StartUpProfileEdit(UpdateAPIView):
    queryset = StartUpProfile.objects.all()
    serializer_class = StartUpProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
