# apps/trivias/views/user_answer_viewset.py
import logging

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from ..models.user_answer import UserAnswer
from ..serializers.user_answer_serializer import UserAnswerSerializer
from ..services.participation_service import ParticipationService

logger = logging.getLogger(__name__)


class UserAnswerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Players to submit their answers.
    Admins can see all, Players only their own.
    """

    serializer_class = UserAnswerSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        queryset = UserAnswer.objects.select_related(
            "participation", "question", "chosen_choice"
        )
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(participation__user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Override create to use the Service Layer for business logic.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participation = serializer.validated_data["participation"]
        question = serializer.validated_data["question"]
        chosen_choice = serializer.validated_data["chosen_choice"]

        try:
            user_answer = ParticipationService.submit_answer(
                participation=participation,
                question=question,
                chosen_choice=chosen_choice,
            )

            logger.info(
                "User %s answered Question %s in Participation %s (Correct: %s)",
                request.user.email,
                question.id,
                participation.id,
                user_answer.is_correct,
            )

            response_serializer = self.get_serializer(user_answer)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                "Error submitting answer for user %s: %s", request.user.email, str(e)
            )
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
