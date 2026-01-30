# apps/trivias/serializers/user_answer_serializer.py
from rest_framework import serializers

from ..models.user_answer import UserAnswer


class UserAnswerSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for User Answers.
    Shows result (is_correct) only if the participation has ended.
    """

    question_text = serializers.ReadOnlyField(source="question.text")
    choice_text = serializers.ReadOnlyField(source="chosen_choice.text")

    class Meta:
        model = UserAnswer
        fields = [
            "id",
            "participation",
            "question",
            "question_text",
            "chosen_choice",
            "choice_text",
            "is_correct",
            "created_at",
        ]
        read_only_fields = ["id", "is_correct", "created_at"]

    def to_representation(self, instance):
        """
        Audit-level rigor: If the user is still playing, we don't leak
        the correctness of the answer to prevent cheating/external aid.
        """
        representation = super().to_representation(instance)

        # If the trivia has NOT ended, we remove the is_correct field from the JSON
        if not instance.participation.end_time:
            representation.pop("is_correct", None)

        return representation
