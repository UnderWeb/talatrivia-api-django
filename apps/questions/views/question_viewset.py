# apps/questions/views/question_viewset.py
import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions, viewsets

from apps.users.enums.user_role import UserRole

from ..models.question import Question
from ..serializers.question_serializer import (
    QuestionPlayerSerializer,
    QuestionSerializer,
)

logger = logging.getLogger(__name__)


@extend_schema_view(
    list=extend_schema(summary="List questions with role-based visibility"),
    retrieve=extend_schema(summary="Get question details"),
    create=extend_schema(summary="Create question with choices (Admin only)"),
)
class QuestionViewSet(viewsets.ModelViewSet):
    """
    Handles Question lifecycle.
    Admins: Full CRUD with correct answer visibility.
    Players: Read-only access to text and options (answers hidden).
    """

    queryset = Question.objects.prefetch_related("choices").all()

    def get_serializer_class(self):
        """
        Ensures players never receive the 'is_correct' field.
        """
        user = self.request.user
        if user.is_staff or (hasattr(user, "role") and user.role == UserRole.ADMIN):
            return QuestionSerializer
        return QuestionPlayerSerializer

    def get_permissions(self):
        """
        Granular access control:
        - Safe methods (GET, HEAD, OPTIONS): Authenticated users.
        - Unsafe methods (POST, PUT, PATCH, DELETE): Admin users only.
        """
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        """Audit log for question creation."""
        question = serializer.save()
        logger.info(
            f"Question ID {question.id} created by Admin: {self.request.user.email}"
        )

    def perform_destroy(self, instance):
        """Audit log for question deletion."""
        logger.warning(
            f"Question ID {instance.id} deleted by Admin: {self.request.user.email}"
        )
        instance.delete()
