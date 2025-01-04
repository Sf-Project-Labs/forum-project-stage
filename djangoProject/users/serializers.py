import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.serializers import Serializer, EmailField, CharField
from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, handling user creation
    and password validation.
    """
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_type', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        """
        Validate the email format to ensure it matches a standard pattern.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        """
        Ensure the password is at least 8 characters long.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return value

    def validate(self, data):
        """
        Validate that password and confirm_password fields match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        """
        Remove confirm_password and create a new user instance.
        """
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(Serializer):
    """
    Serializer for user login, handling validation of credentials.
    """
    email = EmailField()
    password = CharField(write_only=True)

    def validate_email(self, value):
        """
        Validate the email format using Django's validate_email function.
        """
        try:
            validate_email(value)
        except ValidationError as exc:
            raise ValidationError("Invalid email format.") from exc
        return value


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for validating the new password.
    """
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return data

    def validate_new_password(self, value):
        validate_password(value)
        return value