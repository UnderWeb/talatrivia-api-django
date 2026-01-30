# apps/trivias/views/participation_viewset.py
import logging

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models.participation import Participation
from ..serializers.answer_input_serializer import AnswerInputSerializer
from ..serializers.participation_serializer import ParticipationSerializer
from ..services.participation_service import ParticipationService

logger = logging.getLogger(__name__)


class ParticipationViewSet(viewsets.ModelViewSet):
    """
    Handles the lifecycle of a trivia participation.
    Strictly isolated by user and integrated with ParticipationService.
    """

    # queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Multi-level prefetching to avoid N+1 queries during
        game progress review.
        """
        return (
            Participation.objects.filter(user=self.request.user)
            .select_related("user", "trivia")
            .prefetch_related("answers__question", "answers__chosen_choice")
        )

    def perform_create(self, serializer):
        """
        Ensures the participation is linked to the authenticated user.
        """
        participation = serializer.save(user=self.request.user)
        logger.info(
            f"User {self.request.user.email} started trivia {participation.trivia.id}"
        )

    @action(detail=True, methods=["post"], url_path="submit-answer")
    def submit_answer(self, request, pk=None):
        """
        The core engine of the game.
        Validates input and delegates business logic to the Service Layer.
        """
        participation = self.get_object()
        serializer = AnswerInputSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_answer = ParticipationService.submit_answer(
                participation=participation,
                question_id=serializer.validated_data["question_id"],
                choice_id=serializer.validated_data["choice_id"],
            )

            logger.info(
                f"Answer submitted: User {request.user.email} | "
                f"Participation {participation.id} | Question {user_answer.question_id}"
            )

            return Response(
                {"status": "Answer processed successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Unexpected error in submit_answer: {str(e)}", exc_info=True)
            return Response(
                {"error": "An internal error occurred while processing your answer."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
