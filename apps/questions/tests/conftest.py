# apps/questions/tests/conftest.py
"""
pytest fixtures for Questions app.
Provides reusable Question and Choice instances for tests.
"""
import pytest

from apps.questions.tests.factories import ChoiceFactory, QuestionFactory


@pytest.fixture
def question():
    """
    Provides a single Question instance without choices.
    Expected: A Question object with default EASY difficulty.
    """
    return QuestionFactory()


@pytest.fixture
def question_with_choices(question):
    """
    Provides a Question instance with a complete set of choices
    (1 correct, 2 incorrect).
    Expected: A tuple containing the Question and a list of 3 associated Choice objects.
    """
    # Create 2 incorrect choices
    incorrect = ChoiceFactory.create_batch(2, question=question, is_correct=False)
    # Create 1 correct choice
    correct = ChoiceFactory(question=question, is_correct=True)

    choices = incorrect + [correct]
    return question, choices


@pytest.fixture
def correct_choice():
    """
    Provides a standalone Choice instance marked as correct.
    Expected: A Choice object where is_correct is True.
    """
    return ChoiceFactory(is_correct=True)
