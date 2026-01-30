# apps/trivias/views/ranking_view.py
import logging

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.ranking_serializer import RankingSerializer
from ..services.participation_service import ParticipationService

logger = logging.getLogger(__name__)


class TriviaRankingView(APIView):
    """
    Returns the leaderboard for a specific trivia.
    Uses Service Layer for tie-breaking logic (score + time).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, trivia_id):
        logger.info(
            f"User {request.user.email} requested ranking for trivia {trivia_id}"
        )
        ranking_queryset = ParticipationService.get_ranking(trivia_id=trivia_id)

        if not ranking_queryset.exists():
            logger.warning(
                "Ranking requested for trivia %s but no finished participations found.",
                trivia_id,
            )
            return Response(
                {"detail": "No rankings available for this trivia yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = RankingSerializer(ranking_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
