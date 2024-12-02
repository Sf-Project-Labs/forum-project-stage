from rest_framework import serializers
from .models import User
from django.core.exceptions import ValidationError
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_type', 'email', 'password', 'confirm_password']
    
    def validate_email(self, value):
        # Validating the email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        # Ensuring the password is at least 8 characters long
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return value

    def validate(self, data):
        #Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        #Creating a user with validated data
        validated_data.pop('confirm_password', None)
        user = User.objects.create_user(**validated_data)
        return user