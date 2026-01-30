# apps/users/serializers/login_serializer.py
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login request.
    """

    email = serializers.EmailField(
        help_text="User email for authentication.", trim_whitespace=True
    )
    password = serializers.CharField(
        help_text="User password.",
        write_only=True,
        style={"input_type": "password"},
    )
