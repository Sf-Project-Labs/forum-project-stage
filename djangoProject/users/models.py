import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Custom Manager For User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, user_type=None, **extra_fields):
        # Ensure Email Is Provided
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)  # Default Active Status
        extra_fields.setdefault('is_staff', False)  # Default Non-Staff

        # Create User Instance
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)  # Hash The Password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Set Default Values For Superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        # Superuser Does Not Require A User Type
        extra_fields.pop('user_type', None)

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('investor', 'Investor'),
        ('startup', 'Startup'),
        ('both', 'Both'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique Identifier For Each User
    username = models.CharField(max_length=100, null=False, unique=True)  # Unique Username
    first_name = models.CharField(max_length=100, null=False)  # User's First Name
    last_name = models.CharField(max_length=100, null=False)  # User's Last Name
    email = models.EmailField(unique=True, null=False, max_length=255)  # Unique Email Address
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True)  # Type Of User
    password = models.CharField(max_length=255)  # Hashed Password
    is_active = models.BooleanField(default=False)  # Is User Active
    is_staff = models.BooleanField(default=False)  # Is User Staff

    objects = CustomUserManager()  # Custom Manager For User Model

    USERNAME_FIELD = 'email'  # Login Field
    REQUIRED_FIELDS = ['user_type']  # Additional Required Fields

    def __str__(self):
        return self.username