# apps/trivias/serializers/ranking_serializer.py
from rest_framework import serializers

from ..models.participation import Participation


class RankingSerializer(serializers.ModelSerializer):
    """
    Serializer to display the leaderboard.
    Includes calculated duration and user identification.
    """

    user_email = serializers.EmailField(source="user.email", read_only=True)
    duration_seconds = serializers.SerializerMethodField()
    total_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Participation
        fields = ["user_email", "total_score", "duration_seconds", "end_time"]

    def get_duration_seconds(self, obj) -> float:
        """
        Formats the timedelta duration into total seconds.
        Note: 'duration' attribute is injected by ParticipationService.get_ranking
        """
        # We check if 'duration' was annotated in the queryset
        duration = getattr(obj, "duration", None)
        if duration:
            return duration.total_seconds()
        return 0.0
