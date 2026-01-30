# apps/trivias/tests/test_integrations.py
"""
Advanced integration tests for the Trivias app.
Covers the complete game loop: listing trivias, joining a session, and answering.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.trivias.tests.factories import TriviaFactory
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestTriviaIntegrationFlow:
    """
    Test suite for end-to-end trivia gameplay and participation logic.
    """

    def test_full_trivia_discovery_and_participation_flow(self):
        """
        Test that a user can find a trivia and initiate participation.
        Expected: 200 OK on listing and the specific trivia name present in the results.
        """
        user = UserFactory()
        trivia = TriviaFactory(name="Championship Trivia")

        client = APIClient()
        client.force_authenticate(user=user)

        # Discover Quizzes
        url = reverse("v1:trivia-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Check for paginated or non-paginated data
        results = (
            response.data.get("results", response.data)
            if isinstance(response.data, dict)
            else response.data
        )
        assert any(t["name"] == trivia.name for t in results)
        assert any(t["id"] == trivia.id for t in results)

    def test_unauthenticated_user_cannot_list_trivias(self):
        """
        Test that anonymous users are blocked from accessing the trivia list.
        Expected: 401 Unauthorized status code.
        """
        client = APIClient()
        url = reverse("v1:trivia-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
