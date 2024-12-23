"""
Custom User model and manager for the application.

This module defines a custom `User` model and its associated manager,
providing support for flexible user roles and authentication.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.

    Provides methods to create regular users and superusers.
    """

    def create_user(self, email, password=None, user_type=None, **extra_fields):
        """
        Create and return a regular user with the specified email, password, and user type.

        Args:
            email (str): The email address for the user.
            password (str): The user's password.
            user_type (str): The type of user ('investor', 'startup', or 'both').
            **extra_fields: Additional fields to set on the user.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)

        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the specified email and password.

        Args:
            email (str): The email address for the superuser.
            password (str): The superuser's password.
            **extra_fields: Additional fields to set on the superuser.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.pop('user_type', None)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model supporting email-based authentication and user roles.

    Attributes:
        user_id (UUID): Unique identifier for each user.
        username (str): Optional username for the user.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email address (used for authentication).
        user_type (str): The type of user ('investor', 'startup', or 'both').
        password (str): The user's hashed password.
        is_active (bool): Indicates whether the user account is active.
        is_staff (bool): Indicates whether the user has staff permissions.
    """

    USER_TYPE_CHOICES = [
        ('investor', 'Investor'),
        ('startup', 'Startup'),
        ('both', 'Both'),
    ]

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        """
        Return a string representation of the user.

        Returns:
            str: The username if set, otherwise the email.
        """
        return self.username or self.email