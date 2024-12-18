from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.serializers import Serializer, EmailField, CharField
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from rest_framework import status, generics
from .serializers import UserRegistrationSerializer
from .models import User


def home(request):
    return HttpResponse("Welcome to home page")


def health_check(request):
    return JsonResponse({'status': 'ok'})


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


# Serializer for login
class LoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError("Invalid email format.")
        return value


# View for login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(access),
            }, status=status.HTTP_200_OK)

        # Generic error message to prevent information leakage
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
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
