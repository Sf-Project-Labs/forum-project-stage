from rest_framework import serializers
from .models import StartUpProfile


class StartUpProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the `StartUpProfile` model.

    Converts the StartUpProfile model instances to JSON and validates data for creating or updating profiles.
    """
    class Meta:
        model = StartUpProfile
        fields = '__all__'