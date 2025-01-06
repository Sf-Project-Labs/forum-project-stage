from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, generics

from .serializers import UserRegistrationSerializer, LoginSerializer
from .models import User


# Simple Home Page View
def home(request):
    return HttpResponse("Welcome to home page")


# User Registration View
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Serialize and validate the data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the user

        user = serializer.save()
        role = user.user_type

        redirect_url = '/'

        # Redirect based on the role
        if role == "startup":
            redirect_url = f"/profiles/start-up/create/?id_user={user.user_id}"

        return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)


# Login View
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate User With Email And Password
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Generate JWT Tokens For Authenticated User
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'redirect_url': '/'
            }, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# Logout View
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

            # Blacklist The Refresh Token
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
