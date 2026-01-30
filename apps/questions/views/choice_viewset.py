# apps/questions/views/choice_viewset.py
import logging

from rest_framework import permissions, serializers, viewsets

from ..models.choice import Choice
from ..serializers.choice_serializer import ChoiceAdminSerializer

logger = logging.getLogger(__name__)


class ChoiceViewSet(viewsets.ModelViewSet):
    """
    Granular CRUD for Choice model.
    Allows independent corrections (like typos) without affecting the whole question.
    """

    queryset = Choice.objects.select_related("question").all()
    serializer_class = ChoiceAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        """
        Validates business rules even during partial updates.
        Ensures we don't accidentally enable multiple correct answers.
        """
        instance = self.get_object()
        # Check if the update is trying to set is_correct=True
        is_correct = serializer.validated_data.get("is_correct", instance.is_correct)

        if is_correct:
            # Check if another choice for the same question is already correct
            other_correct_exists = (
                Choice.objects.filter(question=instance.question, is_correct=True)
                .exclude(pk=instance.pk)
                .exists()
            )

        if other_correct_exists:
            logger.warning(
                "Integrity violation attempt: Admin %s tried to set "
                "multiple correct answers for Question ID %s",
                self.request.user.email,
                instance.question.id,
            )
            raise serializers.ValidationError(
                {
                    "is_correct": (
                        "This question already has a correct answer. "
                        "Unmark the previous one first."
                    )
                }
            )

        choice = serializer.save()
        logger.info(f"Choice ID {choice.id} updated by {self.request.user.email}")

    def perform_destroy(self, instance):
        """
        Prevents leaving a question with fewer than 2 choices.
        """
        if instance.question.choices.count() <= 2:
            logger.error(
                f"Destruction denied: Admin {self.request.user.email} tried to leave "
                f"Question ID {instance.question.id} with less than 2 choices."
            )
            raise serializers.ValidationError(
                "Cannot delete choice: A question must have at least 2 options."
            )
        choice_id = instance.id
        question_id = instance.question.id
        instance.delete()

        logger.warning(
            (
                f"Choice ID {choice_id} (Question ID {question_id}) "
                f"deleted by {self.request.user.email}"
            )
        )
