# apps/users/tests/test_views.py
"""
Integration tests for User and Auth API views.
Verifies response structures and endpoint accessibility.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserViews:
    """
    Test suite for User-related ViewSets.
    """

    def test_user_list_as_admin(self, api_client, admin_user):
        """
        Test that an administrator can successfully retrieve the paginated
        list of all users.
        Expected: 200 OK and the administrator's email present in the results.
        """
        url = reverse("v1:user-list")
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Handle potential DRF pagination structure
        data = (
            response.data["results"]
            if isinstance(response.data, dict) and "results" in response.data
            else response.data
        )

        emails = [u["email"] for u in data]
        assert admin_user.email in emails

    def test_user_retrieve_own_profile(self, api_client, user):
        """
        Test that a user can access their own detail record via the primary key.
        Expected: 200 OK with matching email and role in the response body.
        """
        url = reverse("v1:user-detail", kwargs={"pk": user.pk})
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
        assert response.data["role"] == user.role

    def test_auth_me_endpoint(self, api_client, user):
        """
        Test that the '/me' shortcut endpoint returns the current authenticated
        user's profile.
        Expected: 200 OK and data matching the authenticated user's email.
        """
        url = reverse("v1:auth-me")
        api_client.force_authenticate(user=user)

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_unauthenticated_request_fails(self, api_client):
        """
        Test that protected user endpoints reject requests from anonymous users.
        Expected: 401 Unauthorized status code.
        """
        url = reverse("v1:user-list")
        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
