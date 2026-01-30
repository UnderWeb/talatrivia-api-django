# apps/users/tests/test_auth_endpoints.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.services.auth_service import AuthService


@pytest.mark.django_db
class TestAuthEndpoints:
    """
    Integration tests for the JWT-based authentication system.
    """

    LOGIN_URL = reverse("v1:auth-login")
    REFRESH_URL = reverse("v1:auth-refresh")
    LOGOUT_URL = reverse("v1:auth-logout")
    ME_URL = reverse("v1:auth-me")

    def test_login_success(self, api_client, user):
        """
        Test that a user can obtain a token pair with valid credentials.
        Expected: 200 OK and tokens in response.
        """
        payload = {"email": user.email, "password": "password123"}
        response = api_client.post(self.LOGIN_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_invalid_credentials(self, api_client, user):
        """
        Test that login fails when providing an incorrect password.
        Expected: 401 Unauthorized.
        """
        payload = {"email": user.email, "password": "wrong_password"}
        response = api_client.post(self.LOGIN_URL, payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_token_refresh_success(self, api_client, user):
        """
        Test the token rotation mechanism using a valid refresh token.
        Expected: 200 OK and a new access token.
        """
        tokens = AuthService.generate_tokens_for_user(user)
        payload = {"refresh": tokens["refresh"]}

        response = api_client.post(self.REFRESH_URL, payload)

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_token_refresh_invalid(self, api_client):
        """
        Test that the system rejects malformed or expired refresh tokens.
        Expected: 401 Unauthorized.
        """
        response = api_client.post(self.REFRESH_URL, {"refresh": "invalid_token"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_endpoint_authenticated(self, api_client, user):
        """
        Test that an authenticated user can retrieve their own profile data.
        Expected: 200 OK and matching email.
        """
        tokens = AuthService.generate_tokens_for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        response = api_client.get(self.ME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_logout_blacklists_token(self, api_client, user):
        """
        Test that logging out blacklists the refresh token to prevent reuse.
        Expected: 204 No Content and TokenError upon subsequent validation.
        """
        tokens = AuthService.generate_tokens_for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        response = api_client.post(self.LOGOUT_URL, {"refresh": tokens["refresh"]})

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(TokenError):
            RefreshToken(tokens["refresh"])

    def test_me_endpoint_unauthenticated(self, api_client):
        """
        Test that an unauthenticated user cannot access the profile endpoint.
        Expected: 401 Unauthorized.
        """
        response = api_client.get(self.ME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_logout_prevents_token_reuse(self, api_client, user):
        """
        Test that a refresh token cannot be used to obtain new tokens after logout.
        Expected: 401 Unauthorized when attempting to refresh.
        """
        tokens = AuthService.generate_tokens_for_user(user)
        refresh_token = tokens["refresh"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

        # 1. Logout
        api_client.post(self.LOGOUT_URL, {"refresh": refresh_token})

        # 2. Attempt to use the same refresh token
        api_client.credentials()  # Clear credentials
        response = api_client.post(self.REFRESH_URL, {"refresh": refresh_token})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
