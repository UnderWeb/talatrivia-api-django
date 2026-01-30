# apps/users/services/auth_service.py
from typing import Dict

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()


class AuthService:
    """
    Service responsible for all authentication-related operations
    using JWT tokens for the User model.
    """

    @staticmethod
    def generate_tokens_for_user(user: User) -> Dict[str, str]:
        """
        Generates a new JWT token pair (access + refresh) for a user.
        """
        refresh = RefreshToken.for_user(user)

        # Optional: add custom claims
        refresh["role"] = user.role
        refresh["email"] = user.email

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    @staticmethod
    def refresh_tokens(refresh_token: str) -> Dict[str, str]:
        """
        Rotates refresh tokens securely.
        Returns a new pair of tokens.
        """
        try:
            refresh = RefreshToken(refresh_token)
            data = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
            refresh.blacklist()
            return data
        except Exception:
            raise ValueError("Invalid refresh token")

    @staticmethod
    def logout(refresh_token: str) -> None:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (TokenError, AttributeError) as e:
            raise ValueError("Token is invalid or already blacklisted") from e
