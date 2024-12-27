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


class InvestorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'
