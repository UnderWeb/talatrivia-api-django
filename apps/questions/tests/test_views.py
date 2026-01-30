# apps/questions/tests/test_views.py
"""
Integration tests for Question and Choice API views.
Verifies endpoint accessibility, response structures, and list data.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.questions.tests.factories import QuestionFactory


@pytest.mark.django_db
class TestQuestionViews:
    """
    Test suite for QuestionViewSet endpoints.
    """

    def test_question_list_authenticated(self, user):
        """
        Test that an authenticated user can successfully retrieve the list of questions.
        Expected: 200 OK and a non-empty list of questions.
        """
        # Ensure data exists
        QuestionFactory.create_batch(2)

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("v1:question-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

        # Handle potential pagination
        data = (
            response.data["results"]
            if isinstance(response.data, dict) and "results" in response.data
            else response.data
        )
        assert len(data) >= 2

    def test_question_list_unauthenticated(self):
        """
        Test that unauthenticated requests to the question list are rejected.
        Expected: 401 Unauthorized.
        """
        client = APIClient()
        url = reverse("v1:question-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_question_detail_endpoint(self, user):
        """
        Test that a specific question can be retrieved by its ID.
        Expected: 200 OK and matching text in the response body.
        """
        question = QuestionFactory(text="Specific Question?")
        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("v1:question-detail", kwargs={"pk": question.pk})
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["text"] == "Specific Question?"
