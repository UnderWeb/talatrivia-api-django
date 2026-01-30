# apps/trivias/models/user_answer.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.questions.models.choice import Choice
from apps.questions.models.question import Question

from .participation import Participation


class UserAnswer(models.Model):
    """
    Represents a user's answer to a specific question in a trivia.
    """

    participation = models.ForeignKey(
        Participation,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name=_("Participation"),
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name=_("Question"),
    )
    chosen_choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="user_answers",
        verbose_name=_("Chosen Choice"),
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Correct Answer"),
        help_text=_(
            "Whether the user's choice was correct. "
            "Persisted to maintain historical scoring."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("User Answer")
        verbose_name_plural = _("User Answers")
        unique_together = [["participation", "question"]]
        indexes = [
            models.Index(fields=["participation", "question"]),
        ]

    def __str__(self):
        status = "Correct" if self.is_correct else "Incorrect"
        return (
            f"{self.participation.user.email} - " f"{self.question.text[:50]}: {status}"
        )
