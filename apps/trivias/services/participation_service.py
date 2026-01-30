# apps/trivias/services/participation_service.py
import logging

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import ExpressionWrapper, F, fields
from django.utils import timezone

from apps.questions.enums.difficulty_level import DifficultyLevel

from ..models.participation import Participation
from ..models.user_answer import UserAnswer

logger = logging.getLogger(__name__)


class ParticipationService:
    """
    Domain service to handle trivia participation logic,
    scoring, and game integrity.
    """

    # Mapping business rules: Difficulty to Points
    DIFFICULTY_POINTS = {
        DifficultyLevel.EASY: 1,
        DifficultyLevel.MEDIUM: 2,
        DifficultyLevel.HARD: 3,
    }

    @staticmethod
    @transaction.atomic
    def submit_answer(participation, question, chosen_choice) -> UserAnswer:
        """
        Processes a user's answer, calculates points, and updates participation.
        """
        # Validation: Is the trivia already finished?
        if participation.is_finished:
            raise ValidationError("This participation has already ended.")

        # Validation: Has this question already been answered in this session?
        if UserAnswer.objects.filter(
            participation=participation, question=question
        ).exists():
            raise ValidationError("Question already answered.")

        # Validation: Does the choice belong to the question?
        if chosen_choice.question_id != question.id:
            raise ValidationError("Invalid choice for this question.")

        # Validation: Does the question belong to the trivia?
        if not participation.trivia.questions.filter(id=question.id).exists():
            raise ValidationError("Question does not belong to this trivia.")

        # Create UserAnswer (is_correct is cached here)
        user_answer = UserAnswer.objects.create(
            participation=participation,
            question=question,
            chosen_choice=chosen_choice,
            is_correct=chosen_choice.is_correct,
        )

        # Scoring Logic: If correct, add points based on difficulty
        if user_answer.is_correct:
            points = ParticipationService.DIFFICULTY_POINTS.get(question.difficulty, 0)
            participation.total_score += points
            participation.save(update_fields=["total_score", "updated_at"])

            logger.info(
                f"User {participation.user.email} scored {points} points "
                f"in Trivia {participation.trivia.id}"
            )

        return user_answer

    @staticmethod
    def finish_participation(participation):
        """
        Closes the participation session and records the end time.
        """
        if not participation.is_finished:
            participation.end_time = timezone.now()
            participation.save(update_fields=["end_time", "updated_at"])
            logger.info(
                f"Participation {participation.id} finished at {participation.end_time}"
            )
        return participation

    @staticmethod
    def get_ranking(trivia_id=None, limit=10):
        """
        Calculates the leaderboard.
        Primary sort: Highest total_score.
        Secondary sort (Tie-breaker): Shortest duration.
        """
        queryset = Participation.objects.filter(end_time__isnull=False)

        if trivia_id:
            queryset = queryset.filter(trivia_id=trivia_id)

        # ExpressionWrapper to perform the duration calculation.
        # Duration = end_time - start_time
        ranking = (
            queryset.select_related("user")
            .annotate(
                duration=ExpressionWrapper(
                    F("end_time") - F("start_time"), output_field=fields.DurationField()
                )
            )
            .order_by(
                "-total_score",  # Primary: More points is better
                "duration",  # Secondary (Tie-breaker): Less time is better
            )[:limit]
        )

        return ranking
