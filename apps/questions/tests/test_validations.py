# apps/questions/tests/test_validations.py
"""
Validation tests for Question and Choice models.
Covers required fields, database constraints, and model relationships.
"""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.questions.models.choice import Choice
from apps.questions.models.question import Question
from apps.questions.tests.factories import QuestionFactory


@pytest.mark.django_db
class TestQuestionValidations:
    """
    Test suite for hard constraints and validation rules in the Questions app.
    """

    def test_question_text_required(self):
        """
        Test that a Question cannot be created without text content.
        Expected: IntegrityError raised due to NOT NULL constraint in the database.
        """
        with pytest.raises(IntegrityError):
            Question.objects.create(text=None, difficulty="EASY")

    def test_choice_requires_question(self):
        """
        Test that a Choice must be associated with a Question instance.
        Expected: IntegrityError raised when attempting to create a choice
        with no question.
        """
        with pytest.raises(IntegrityError):
            Choice.objects.create(text="Option A", is_correct=False, question=None)

    def test_question_invalid_difficulty(self):
        """
        Test that providing an invalid difficulty value triggers a validation error.
        Expected: ValidationError raised during the model's full_clean() method.
        """
        question = QuestionFactory.build(difficulty="EXTREME")
        with pytest.raises(ValidationError):
            question.full_clean()
