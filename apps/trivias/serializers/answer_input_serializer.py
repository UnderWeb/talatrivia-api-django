# apps/trivias/serializers/answer_input_serializer.py
from rest_framework import serializers


class AnswerInputSerializer(serializers.Serializer):
    """
    DTO for submitting an answer.
    Keeps the input clean and easy to validate.
    """

    question_id = serializers.IntegerField(required=True)
    choice_id = serializers.IntegerField(required=True)
