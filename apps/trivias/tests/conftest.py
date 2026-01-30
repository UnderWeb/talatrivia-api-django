# apps/trivias/tests/conftest.py
"""
pytest fixtures for the Trivias app.
Provides reusable Trivia, Participation,
and UserAnswer instances for testing game logic.
"""
import pytest

from apps.trivias.tests.factories import (
    ParticipationFactory,
    TriviaFactory,
    UserAnswerFactory,
)
from apps.users.tests.factories import UserFactory


@pytest.fixture
def user():
    """
    Provides a regular User instance.
    Expected: A User object with default role and randomized data.
    """
    return UserFactory()


@pytest.fixture
def trivia():
    """
    Provides a standalone Trivia instance.
    Expected: A Trivia object with a randomized name.
    """
    return TriviaFactory()


@pytest.fixture
def participation(user, trivia):
    """
    Provides a Participation instance linking a user and a specific trivia.
    Expected: A Participation object connecting the provided user and trivia.
    """
    return ParticipationFactory(user=user, trivia=trivia)


@pytest.fixture
def user_answer(participation):
    """
    Provides a UserAnswer instance linked to a participation session.
    Expected: A UserAnswer object with an associated question and choice.
    """
    return UserAnswerFactory(participation=participation)
