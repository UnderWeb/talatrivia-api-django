# apps/trivias/tests/test_models.py
"""
Unit tests for Trivia, Participation, and UserAnswer models.
Verifies model creation, integrity constraints, and multi-level relationships.
"""
import pytest

from apps.trivias.models.participation import Participation
from apps.trivias.models.trivia import Trivia
from apps.trivias.models.user_answer import UserAnswer
from apps.trivias.tests.factories import (
    ParticipationFactory,
    TriviaFactory,
    UserAnswerFactory,
)


@pytest.mark.django_db
class TestTriviaModels:
    """
    Test suite for the core game logic models in the Trivias app.
    """

    def test_trivia_creation(self):
        """
        Test that a Trivia session can be successfully created.
        Expected: The trivia instance has a valid name and is correctly saved.
        """
        trivia = TriviaFactory(name="General Knowledge")
        assert isinstance(trivia, Trivia)
        assert trivia.name == "General Knowledge"

    def test_participation_and_user_answer_flow(self, user):
        """
        Test the relationship chain from User to UserAnswer through Participation.
        Expected: All entities are correctly linked and the answer's
        participation matches.
        """
        trivia = TriviaFactory()
        participation = ParticipationFactory(user=user, trivia=trivia)
        user_answer = UserAnswerFactory(participation=participation)

        assert isinstance(participation, Participation)
        assert participation.user == user
        assert user_answer.participation == participation
        assert isinstance(user_answer, UserAnswer)

    def test_user_answer_correctness_logic(self):
        """
        Test that UserAnswer correctly identifies if the chosen choice is the right one.
        Expected: The is_correct field matches the underlying choice's status.
        """
        # Create an answer where we know the choice is correct
        answer = UserAnswerFactory(chosen_choice__is_correct=True)
        assert answer.is_correct is True

        # Create an answer where we know the choice is incorrect
        wrong_answer = UserAnswerFactory(chosen_choice__is_correct=False)
        assert wrong_answer.is_correct is False
