from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import StartUpProfile, InvestorProfile

User = get_user_model()


class StartUpProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StartUpProfile
        fields = ['id', 'user', 'company_name', 'legal_name', 'project_information']  # Include all required fields
        read_only_fields = ['user', ]

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid user ID.")
        return value

    def validate_company_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Company name must be at least 3 characters long.")
        return value

    def validated_legal_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Company name must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user  # Associate the current user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            raise serializers.ValidationError("User cannot be updated.")
        return super().update(instance, validated_data)


class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = ['id', 'user', 'company_name', 'legal_name']

    def validate_user(self, value):
        if not User.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid user ID.")
        return value

    def validate_company_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Company name must be at least 3 characters long.")
        return value

    def validated_legal_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Company name must be at least 3 characters long.")
        return value
