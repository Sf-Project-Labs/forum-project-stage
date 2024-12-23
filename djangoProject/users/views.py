"""
Views for user-related operations, including registration, login, and logout.
"""

from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, generics

from .serializers import UserRegistrationSerializer, LoginSerializer
from .models import User


def home(request):
    """
    Simple view to display the home page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A simple welcome message.
    """
    return HttpResponse("Welcome to home page")


class UserRegistrationView(generics.CreateAPIView):
    """
    API view to handle user registration.

    Allows users to create a new account by providing
    the required fields.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    """
    API view to handle user login.

    Validates user credentials and returns JWT tokens upon success.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request to authenticate user and issue tokens.

        Args:
            request: The HTTP request object containing login data.

        Returns:
            Response: JSON containing refresh and access tokens if successful,
                      or error message if authentication fails.
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(access),
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    """
    API view to handle user logout.

    Requires a valid refresh token to blacklist it.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle POST request to logout user by blacklisting the refresh token.

        Args:
            request: The HTTP request object containing the refresh token.

        Returns:
            Response: Success message or error details.
        """
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required for logout."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
