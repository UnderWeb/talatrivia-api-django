# apps/trivias/views/trivia_viewset.py
import logging

from rest_framework import permissions, viewsets

from ..models.trivia import Trivia
from ..serializers.trivia_serializer import TriviaSerializer

logger = logging.getLogger(__name__)


class TriviaViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and retrieving Trivias.
    Use ReadOnlyModelViewSet to prevent players from creating/deleting games.
    """

    serializer_class = TriviaSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Optimized query to avoid N+1 problem when fetching questions and choices.
        """
        return Trivia.objects.prefetch_related(
            "trivia_questions__question__choices"
        ).all()

    def list(self, request, *args, **kwargs):
        logger.info(f"User {request.user.email} is listing available trivias.")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.info(
            "User %s accessed trivia detail: %s (ID: %s)",
            request.user.email,
            instance.name,
            instance.id,
        )
        return super().retrieve(request, *args, **kwargs)
