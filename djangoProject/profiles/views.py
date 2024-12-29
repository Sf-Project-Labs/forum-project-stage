from django.contrib.auth import get_user_model
from .serializers import StartUpProfileSerializer, InvestorProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

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
            raise ValueError("User ID is missing in the query parameters.")

        # Get the User instance based on the id_user
        user = get_object_or_404(User, user_id=id_user)

        # Save the StartupProfile with the associated user
        serializer.save(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['id_user'] = self.request.query_params.get('id_user')
        return context
