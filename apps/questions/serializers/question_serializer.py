# apps/questions/serializers/question_serializer.py
from django.db import transaction
from rest_framework import serializers

from ..models.choice import Choice
from ..models.question import Question
from .choice_serializer import ChoiceAdminSerializer, ChoicePlayerSerializer


class QuestionSerializer(serializers.ModelSerializer):
    """
    Admin-facing serializer. Handles nested creation of choices.
    """

    choices = ChoiceAdminSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "difficulty", "choices", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_choices(self, value):
        """
        Business Logic Validation:
        1. Minimum 2 options.
        2. Exactly ONE correct answer.
        """
        if len(value) < 2:
            raise serializers.ValidationError(
                "A question must have at least two choices."
            )

        correct_answers = [
            choice for choice in value if choice.get("is_correct") is True
        ]
        if len(correct_answers) != 1:
            raise serializers.ValidationError(
                "A question must have exactly ONE correct answer."
            )

        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Creates a Question and its Choices in a single atomic transaction.
        """
        choices_data = validated_data.pop("choices")
        question = Question.objects.create(**validated_data)

        # Bulk create
        choice_instances = [
            Choice(question=question, **choice_data) for choice_data in choices_data
        ]
        Choice.objects.bulk_create(choice_instances)

        return question


class QuestionPlayerSerializer(serializers.ModelSerializer):
    """
    Player-facing serializer. Used during trivia gameplay.
    """

    choices = ChoicePlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "choices"]
