# apps/trivias/serializers/participation_serializer.py
from rest_framework import serializers

from ..models.participation import Participation
from .user_answer_serializer import UserAnswerSerializer


class ParticipationSerializer(serializers.ModelSerializer):
    answers = UserAnswerSerializer(many=True, read_only=True)
    trivia_name = serializers.ReadOnlyField(source="trivia.name")
    duration = serializers.ReadOnlyField(source="duration_seconds")

    class Meta:
        model = Participation
        fields = [
            "id",
            "user",
            "trivia",
            "trivia_name",
            "start_time",
            "end_time",
            "duration",
            "total_score",
            "answers",
        ]
        read_only_fields = [
            "id",
            "user",
            "start_time",
            "total_score",
            "answers",
        ]
