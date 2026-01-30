# apps/trivias/tests/test_permissions.py
"""
Permission tests for the Trivias app.
Ensures strict data isolation between users as per Talatrivia requirements.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.trivias.tests.factories import ParticipationFactory, TriviaFactory
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestTriviaPermissions:
    """
    Test suite for access control on Participation endpoints.
    Verifies that the 'Strictly isolated by user' policy is enforced.
    """

    def test_user_cannot_see_others_participation(self):
        """
        Test that the API enforces strict isolation by user.
        Expected: A user only sees their own records, even if others exist.
        """
        user1 = UserFactory()
        user2 = UserFactory()
        trivia = TriviaFactory()

        # Create records for both users
        ParticipationFactory(user=user1, trivia=trivia)
        ParticipationFactory(user=user2, trivia=trivia)

        client = APIClient()
        client.force_authenticate(user=user1)

        url = reverse("v1:participation-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Handling potential ReturnList (non-paginated)
        results = (
            response.data
            if isinstance(response.data, list)
            else response.data.get("results", [])
        )

        # Should only see user1's participation
        assert len(results) == 1
        assert results[0]["user"] == user1.pk

    def test_admin_is_also_isolated_by_default(self, admin_user):
        """
        Test that even an admin user is subject to isolation if they have
        no personal records.
        Expected: 200 OK and an empty list if the admin hasn't participated
        in any trivia.
        """
        # Create data for other users
        ParticipationFactory(user=UserFactory())
        ParticipationFactory(user=UserFactory())

        client = APIClient()
        client.force_authenticate(user=admin_user)

        url = reverse("v1:participation-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        results = (
            response.data
            if isinstance(response.data, list)
            else response.data.get("results", [])
        )

        # Current implementation in ParticipationViewSet filters
        # strictly by request.user
        # Since admin_user has no participations, results must be 0
        assert len(results) == 0
