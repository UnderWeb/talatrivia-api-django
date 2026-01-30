# apps/trivias/models/trivia.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.questions.models.question import Question


class Trivia(models.Model):
    """
    Represents a trivia game containing multiple questions.
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_("Trivia Name"),
        help_text=_("The display name of the trivia game."),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("A short description of this trivia."),
    )
    questions = models.ManyToManyField(
        Question,
        through="TriviaQuestion",
        related_name="trivias",
        verbose_name=_("Questions"),
        help_text=_("The set of questions included in this trivia."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Trivia")
        verbose_name_plural = _("Trivias")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
