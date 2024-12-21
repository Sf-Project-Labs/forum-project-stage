from rest_framework import serializers
from .models import User
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.serializers import Serializer, EmailField, CharField

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Define Fields For Registration
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_type', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        # Validate Email Format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        # Ensure Password Is At Least 8 Characters Long
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return value

    def validate(self, data):
        # Check That Password And Confirm Password Match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove Confirm Password Before Creating The User
        validated_data.pop('confirm_password', None)

        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(Serializer):
    # Define Fields For Login
    email = EmailField()
    password = CharField(write_only=True)

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise ValidationError("Invalid email format.")
        return value
