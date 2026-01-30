# apps/users/tests/test_permissions.py
"""
Permissions and Access Control tests for the Users app.
Verifies that only authorized users can access or modify specific resources.
"""
import pytest
from django.urls import reverse
from rest_framework import status

from apps.users.tests.factories import PlayerFactory


@pytest.mark.django_db
class TestUserPermissions:
    """
    Suite to verify RBAC (Role-Based Access Control) across User endpoints.
    """

    def test_admin_can_access_user_list(self, api_client, admin_user):
        """
        Test that an administrator can successfully retrieve the complete user list.
        Expected: 200 OK.
        """
        url = reverse("v1:user-list")
        api_client.force_authenticate(user=admin_user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_player_is_restricted_from_list(self, api_client, user):
        """
        Test that a regular player is restricted to seeing only their own record
        in the list.
        Expected: 200 OK and a result count of 1 containing the user's email.
        """
        url = reverse("v1:user-list")
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.data["results"] if "results" in response.data else response.data
        assert len(data) == 1
        assert data[0]["email"] == user.email

    def test_user_cannot_access_other_user_detail(self, api_client, user):
        """
        Test that a user cannot access another user's detail view.
        Expected: 404 Not Found to maintain resource obfuscation.
        """
        other_user = PlayerFactory()
        url = reverse("v1:user-detail", args=[other_user.pk])
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_can_access_own_detail(self, api_client, user):
        """
        Test that a user can successfully retrieve their own profile details.
        Expected: 200 OK and matching email in response.
        """
        url = reverse("v1:user-detail", args=[user.pk])
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email
