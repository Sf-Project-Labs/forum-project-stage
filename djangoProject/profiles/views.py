from django.contrib.auth import get_user_model
from jwt import InvalidTokenError
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import UntypedToken, AccessToken

from .serializers import StartUpProfileSerializer, InvestorProfileSerializer
from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import StartUpProfile
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings

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

    def get_object(self):
        # Get the object using the standard lookup field
        obj = super().get_object()

        # Extract the Authorization header
        auth_header = self.request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Missing or invalid Authorization header.")

        # Extract and decode the access token
        token_str = auth_header.split(" ")[1]
        try:
            # Decode the access token
            token = AccessToken(token_str)
            edit_id = self.kwargs.get(self.lookup_field)

            profile_to_edit = StartUpProfile.objects.get(id=edit_id)
            user_id = profile_to_edit.user.user_id

            # Ensure the token belongs to the currently authenticated user
            if str(user_id) != str(self.request.user.user_id):
                print(user_id)
                print(self.request.user.user_id)
                raise PermissionDenied("You are not authorized to edit this profile.")
        except Exception as e:
            raise PermissionDenied(f"Invalid token: {str(e)}")

        # Ensure the object belongs to the authenticated user
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this profile.")

        return obj