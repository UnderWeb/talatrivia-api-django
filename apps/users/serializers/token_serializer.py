# apps/users/serializers/token_serializer.py
from rest_framework import serializers


class TokenPairSerializer(serializers.Serializer):
    """
    Serializer for JWT pair response.
    """

    access = serializers.CharField(help_text="Access token for API requests.")
    refresh = serializers.CharField(
        help_text="Refresh token to obtain new access token."
    )


class RefreshSerializer(serializers.Serializer):
    """
    Serializer for refreshing access token.
    """

    refresh = serializers.CharField(help_text="Refresh token issued previously.")


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for logout request using refresh token.
    """

    refresh = serializers.CharField(
        help_text="Refresh token to be blacklisted on logout."
    )
