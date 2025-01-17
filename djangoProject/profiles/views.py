from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied, AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .serializers import StartUpProfileSerializer
from .models import StartUpProfile

User = get_user_model()


class StartupProfileViewSet(ViewSet):
    """
    A ViewSet to handle startup profile actions: registration, retrieval, and update.
    """
    permission_classes = [IsAuthenticated]

    def create(self, request):
        """Handles Startup Registration."""
        id_user = request.query_params.get('id_user')
        if not id_user:
            raise ValidationError("User ID is missing in the query parameters.")

        # Get the user instance
        user = get_object_or_404(User, user_id=id_user)

        # Save the startup profile
        serializer = StartUpProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        """Handles retrieving a single startup profile."""
        profile = get_object_or_404(StartUpProfile, pk=pk)
        serializer = StartUpProfileSerializer(profile)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handles updating a startup profile."""
        profile = get_object_or_404(StartUpProfile, pk=pk)
        self._check_user_permissions(request, profile)

        # Update and save the profile
        serializer = StartUpProfileSerializer(profile, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Handles partial updates to a startup profile."""
        profile = get_object_or_404(StartUpProfile, pk=pk)
        self._check_user_permissions(request, profile)

        # Partially update and save the profile
        serializer = StartUpProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def _check_user_permissions(self, request, profile):
        """Checks if the authenticated user has permission to modify the profile."""
        auth_header = request.headers.get("Authorization", None)
        if not auth_header or not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Missing or invalid Authorization header.")

        token_str = auth_header.split(" ")[1]
        token = AccessToken(token_str)
        user_id = profile.user.user_id

        if str(user_id) != str(request.user.user_id):
            raise PermissionDenied("You are not authorized to edit this profile.")

        if profile.user != request.user:
            raise PermissionDenied("You do not have permission to edit this profile.")

