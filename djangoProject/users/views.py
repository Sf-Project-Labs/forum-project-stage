from datetime import timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.http import HttpResponse
from django.utils.timezone import now
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, generics
from .models import User, TokenRecord
from .serializers import UserRegistrationSerializer, LoginSerializer, PasswordResetSerializer
from djangoProject import settings


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
            redirect_url = f"/profiles/start-up/?id_user={user.user_id}"

        return Response({"redirect_url": redirect_url}, status=status.HTTP_200_OK)


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

            TokenRecord.objects.create(
                user=user,
                access_token=str(access),
                refresh_token=str(refresh),
                expires_at=now() + timedelta(days=1)
            )

            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'redirect_url': '/'
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
            token_record_obj = TokenRecord.objects.filter(refresh_token=refresh_token)
            TokenRecord.delete(token_record_obj)

            return Response(
                {"message": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordRecoveryView(APIView):
    """
    API view for initiating the password recovery process.

    Sends a password recovery email to the user if the provided email exists.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to initiate password recovery.

        Args:
            request (HttpRequest): The HTTP request object containing the user's email.

        Returns:
            Response: A response indicating whether the recovery email was sent.
        """
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "If the email exists, a recovery email has been sent."},
                status=status.HTTP_200_OK
            )

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = request.build_absolute_uri(f"/password-reset/?uid={uid}&token={token}")

        send_mail(
            subject="Password Recovery",
            message=f"Click the link to reset your password: {reset_link}\n"
                    "This link will expire once used or when the password is successfully reset.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return Response(
            {"detail": "If the email exists, a recovery email has been sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetView(APIView):
    """
    API view for resetting a user's password.

    Verifies the token and UID, then updates the user's password if valid.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST requests to reset a user's password.

        Args:
            request (HttpRequest): The HTTP request object containing the new password,
                                   token, and UID.

        Returns:
            Response: A response indicating the result of the password reset process.
        """
        uid = request.GET.get("uid")
        token = request.GET.get("token")

        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data["new_password"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid token or user ID. Ensure the link is correct and not expired"}, status.HTTP_400_BAD_REQUEST
            )

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."}, status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password reset successful."}, status.HTTP_200_OK
        )