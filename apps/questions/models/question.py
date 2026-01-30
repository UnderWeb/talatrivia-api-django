# apps/questions/models/question.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.difficulty_level import DifficultyLevel


class Question(models.Model):
    """
    Represents a trivia question in the system.
    """

    text = models.TextField(
        verbose_name=_("Question Text"),
        help_text=_("The text of the question to be presented to the player."),
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.EASY,
        verbose_name=_("Difficulty Level"),
        db_index=True,
        help_text=_("The difficulty level determines scoring for this question."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"
