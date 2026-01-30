# apps/questions/tests/test_serializers.py
"""
Unit tests for Question and Choice serializers.
Validates object serialization, nested relationships, and field mapping.
"""
import pytest

from apps.questions.serializers.question_serializer import QuestionSerializer
from apps.questions.tests.factories import ChoiceFactory, QuestionFactory


@pytest.mark.django_db
class TestQuestionSerializer:
    """
    Test suite for QuestionSerializer logic and nested Choice mapping.
    """

    def test_question_serializer_output(self):
        """
        Test that the serializer correctly maps Question fields to JSON.
        Expected: 'text' and 'difficulty' in the output match the model instance.
        """
        question = QuestionFactory(
            text="Is Python a programming language?", difficulty="EASY"
        )
        serializer = QuestionSerializer(question)

        assert serializer.data["text"] == question.text
        assert serializer.data["difficulty"] == "EASY"

    def test_question_serializer_with_nested_choices(self, question):
        """
        Test that the serializer includes associated choices in its output.
        Expected: A 'choices' field exists and contains the serialized Choice objects.
        """
        # Create a choice for the question
        ChoiceFactory(question=question, text="Yes", is_correct=True)

        serializer = QuestionSerializer(question)

        assert "choices" in serializer.data
        assert len(serializer.data["choices"]) == 1
        assert serializer.data["choices"][0]["text"] == "Yes"
        assert serializer.data["choices"][0]["is_correct"] is True
