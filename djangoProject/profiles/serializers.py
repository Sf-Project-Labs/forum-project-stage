from rest_framework import serializers
from .models import StartUpProfile, InvestorProfile


class StartUpProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartUpProfile
        fields = ['id', 'user', 'startup_name', 'startup_description']  # Include all required fields

    def validate_user(self, value):
        # Optional: Validate that the user exists
        from django.contrib.auth.models import User
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid user ID.")
        return value


class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'
