# apps/trivias/tests/test_views.py
"""
Integration tests for Trivia and Participation views.
Verifies participation creation flow and data integrity.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.questions.tests.factories import ChoiceFactory, QuestionFactory
from apps.trivias.models.trivia_question import TriviaQuestion
from apps.trivias.models.user_answer import UserAnswer
from apps.trivias.tests.factories import ParticipationFactory, TriviaFactory


@pytest.mark.django_db
class TestTriviaViews:
    """
    Test suite for Trivia and Participation endpoints.
    """

    def test_trivia_list_endpoint(self, user):
        """
        Test that an authenticated user can retrieve the available trivias.
        Expected: 200 OK and a list of trivia data.
        """
        TriviaFactory.create_batch(2)
        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("v1:trivia-list")
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        results = (
            response.data
            if isinstance(response.data, list)
            else response.data.get("results", [])
        )
        assert len(results) >= 1

    def test_create_participation_automated_user_binding(self, user):
        """
        Test that creating a participation successfully links the trivia and the user.
        Expected: 201 Created.
        """
        trivia = TriviaFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("v1:participation-list")
        data = {"trivia": trivia.id}

        response = client.post(url, data, format="json")

        assert (
            response.status_code == status.HTTP_201_CREATED
        ), f"Errors: {response.data}"
        assert response.data["user"] == user.id
        assert response.data["trivia"] == trivia.id

    def test_submit_answer_and_verify_correctness(self, user):
        """
        Test that a player can submit an answer and it is marked as correct
        in the database.
        Expected: 201 Created and UserAnswer exists with is_correct=True.
        """
        trivia = TriviaFactory()
        question = QuestionFactory(difficulty="HARD")
        choice = ChoiceFactory(question=question, is_correct=True)
        TriviaQuestion.objects.create(trivia=trivia, question=question, order=1)
        participation = ParticipationFactory(user=user, trivia=trivia)

        client = APIClient()
        client.force_authenticate(user=user)

        url = reverse("v1:user-answer-list")
        data = {
            "participation": participation.id,
            "question": question.id,
            "chosen_choice": choice.id,
        }

        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        answer_exists = UserAnswer.objects.filter(
            participation=participation, question=question, is_correct=True
        ).exists()
        assert answer_exists is True

    def test_cannot_answer_same_question_twice(self, user):
        """
        Test that a player cannot answer the same question more than once
        in the same session.
        Expected: 400 Bad Request on the second attempt.
        """
        trivia = TriviaFactory()
        question = QuestionFactory()
        choice = ChoiceFactory(question=question)
        TriviaQuestion.objects.create(trivia=trivia, question=question, order=1)
        participation = ParticipationFactory(user=user, trivia=trivia)

        client = APIClient()
        client.force_authenticate(user=user)
        url = reverse("v1:user-answer-list")
        data = {
            "participation": participation.id,
            "question": question.id,
            "chosen_choice": choice.id,
        }

        client.post(url, data, format="json")
        response = client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
