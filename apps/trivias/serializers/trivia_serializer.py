# apps/trivias/serializers/trivia_serializer.py
from rest_framework import serializers

from apps.questions.serializers.question_serializer import QuestionPlayerSerializer

from ..models.trivia import Trivia
from ..models.trivia_question import TriviaQuestion


class TriviaQuestionSerializer(serializers.ModelSerializer):
    """
    Nests the question data using the Player-safe serializer.
    """

    question = QuestionPlayerSerializer(read_only=True)

    class Meta:
        model = TriviaQuestion
        fields = ["question", "order"]


class TriviaSerializer(serializers.ModelSerializer):
    """
    Main Trivia serializer.
    Uses 'trivia_questions' (the related_name from TriviaQuestion model)
    to maintain the defined order.
    """

    questions = TriviaQuestionSerializer(
        source="trivia_questions", many=True, read_only=True
    )

    write_questions = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )

    class Meta:
        model = Trivia
        fields = [
            "id",
            "name",
            "description",
            "questions",
            "write_questions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        questions_data = validated_data.pop("write_questions", None)
        instance = super().update(instance, validated_data)

        if questions_data is not None:
            instance.trivia_questions.all().delete()

            for item in questions_data:
                TriviaQuestion.objects.create(
                    trivia=instance, question_id=item["question"], order=item["order"]
                )
        return instance
