# apps/users/tests/test_services.py
"""
Unit tests for AuthService.
Validates JWT lifecycle management: generation, rotation, and blacklisting.
"""
import pytest
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.services.auth_service import AuthService


@pytest.mark.django_db
class TestAuthService:
    """
    Test suite for Auth service logic.
    Ensures security tokens are handled according to business rules.
    """

    def test_generate_tokens_for_user(self, user):
        """
        Test that the service generates a valid token pair with custom user claims.
        Expected: A dictionary with 'access' and 'refresh' tokens containing correct
        role and email.
        """
        tokens = AuthService.generate_tokens_for_user(user)

        assert "access" in tokens
        assert "refresh" in tokens

        # Verify custom claims in token
        refresh = RefreshToken(tokens["refresh"])
        assert refresh["role"] == user.role
        assert refresh["email"] == user.email

    def test_refresh_tokens_rotates_and_invalidates_old_one(self, user):
        """
        Test that refreshing tokens issues a new set and blacklists
        the previous refresh token.
        Expected: New tokens are returned and the old refresh token raises
        TokenError upon reuse.
        """
        original_tokens = AuthService.generate_tokens_for_user(user)
        old_refresh = original_tokens["refresh"]

        # Execution of the rotation service
        new_tokens = AuthService.refresh_tokens(old_refresh)

        assert "access" in new_tokens
        assert "refresh" in new_tokens

        # Security check: The old token must be blacklisted immediately
        with pytest.raises(TokenError):
            RefreshToken(old_refresh)

    def test_logout_blacklists_token_successfully(self, user):
        """
        Test that the logout service correctly invalidates the provided refresh token.
        Expected: The token is added to the blacklist and cannot be instantiated again.
        """
        tokens = AuthService.generate_tokens_for_user(user)
        refresh_token = tokens["refresh"]

        AuthService.logout(refresh_token)

        with pytest.raises(TokenError):
            RefreshToken(refresh_token)

    def test_refresh_with_invalid_token_raises_error(self):
        """
        Test that providing a malformed or invalid token to the refresh service
        triggers an exception.
        Expected: A ValueError or Exception is raised, preventing further processing.
        """
        with pytest.raises(Exception):
            AuthService.refresh_tokens("not.a.valid.token")
