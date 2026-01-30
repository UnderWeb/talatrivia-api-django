# apps/users/serializers/me_serializer.py
from rest_framework import serializers

from ..models.user import User


class MeSerializer(serializers.ModelSerializer):
    """
    Serializer for current user data.
    """

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role"]
        read_only_fields = fields
