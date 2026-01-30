# apps/trivias/tests/test_serializers.py
"""
Unit tests for Trivia serializers.
Validates data validation, object creation, and field mapping for Trivia models.
"""
import pytest

from apps.trivias.serializers.trivia_serializer import TriviaSerializer
from apps.trivias.tests.factories import TriviaFactory


@pytest.mark.django_db
class TestTriviaSerializer:
    """
    Test suite for TriviaSerializer validation and serialization logic.
    """

    def test_trivia_serialization_valid_data(self):
        """
        Test that the serializer correctly validates and saves a new Trivia instance.
        Expected: is_valid() returns True and the saved instance matches the input data.
        """
        data = {"name": "My Trivia", "description": "A necessary description"}
        serializer = TriviaSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

        trivia = serializer.save()
        assert trivia.name == "My Trivia"
        assert trivia.description == "A necessary description"

    def test_trivia_serialization_output(self):
        """
        Test that the serializer produces the expected dictionary output from
        an instance.
        Expected: The serialized data contains the 'id', 'name',
        and 'description' fields.
        """
        trivia = TriviaFactory(name="Output Test", description="Checking fields")
        serializer = TriviaSerializer(instance=trivia)

        assert serializer.data["name"] == "Output Test"
        assert "id" in serializer.data
        assert serializer.data["description"] == "Checking fields"
