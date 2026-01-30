# apps/trivias/models/trivia_question.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.questions.models.question import Question

from .trivia import Trivia


class TriviaQuestion(models.Model):
    """
    Intermediate table for ordering questions within a trivia.
    """

    trivia = models.ForeignKey(
        Trivia,
        on_delete=models.CASCADE,
        related_name="trivia_questions",
        verbose_name=_("Trivia"),
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="trivia_questions",
        verbose_name=_("Question"),
    )
    order = models.PositiveIntegerField(
        verbose_name=_("Order"),
        help_text=_("Defines the order of questions in the trivia."),
    )

    class Meta:
        verbose_name = _("Trivia Question")
        verbose_name_plural = _("Trivia Questions")
        unique_together = [["trivia", "question"]]
        ordering = ["-trivia__created_at", "order"]
        indexes = [
            models.Index(fields=["trivia", "order"]),
        ]

    def __str__(self):
        return f"{self.trivia.name} - Q{self.order}: {self.question.text[:50]}"
