# apps/questions/tests/test_models.py
"""
Unit tests for Question and Choice models.
Verifies model creation, relationships, and string representations.
"""
import pytest

from apps.questions.models.choice import Choice
from apps.questions.models.question import Question
from apps.questions.tests.factories import ChoiceFactory, QuestionFactory


@pytest.mark.django_db
class TestQuestionModels:
    """
    Test suite for the integrity of Question and Choice models.
    """

    def test_question_creation(self):
        """
        Test that a Question instance can be correctly created using the factory.
        Expected: The instance is a Question type and the string includes text
        and difficulty.
        """
        text = "What is the capital of Chile?"
        question = QuestionFactory(text=text, difficulty="EASY")

        assert isinstance(question, Question)
        # Matching the actual __str__ logic: "Text (DIFFICULTY)"
        assert str(question) == f"{text} (EASY)"

    def test_choice_creation_and_relationship(self, question):
        """
        Test that a Choice can be linked to a Question and stores data correctly.
        Expected: The choice links to the question and the string includes
        correctness status.
        """
        text = "Santiago"
        choice = ChoiceFactory(question=question, text=text, is_correct=False)

        assert choice.question == question
        assert isinstance(choice, Choice)
        # Matching the actual __str__ logic: "Text (Incorrect/Correct)"
        assert str(choice) == f"{text} (Incorrect)"

    def test_question_difficulty_choices(self):
        """
        Test that the question difficulty is stored correctly based on choices.
        Expected: The difficulty matches the value assigned during creation.
        """
        question = QuestionFactory(difficulty="HARD")
        assert question.difficulty == "HARD"
