import re
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User

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

        # Generate Username If Not Provided
        if 'username' not in validated_data or not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]

        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    # Define Fields For Login
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Authenticate User
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")

        data['user'] = user
        return data
