# apps/questions/models/choice.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from .question import Question


class Choice(models.Model):
    """
    Represents a selectable answer option for a Question.
    """

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices",
        verbose_name=_("Question"),
        help_text=_("The question this choice belongs to."),
    )
    text = models.TextField(
        verbose_name=_("Answer Text"), help_text=_("The text of the answer option.")
    )
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Correct Answer"),
        help_text=_("Marks if this choice is the correct answer."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")
        unique_together = [["question", "text"]]
        ordering = ["id"]
        constraints = [
            # 1. Prevent duplicate text for the same question
            models.UniqueConstraint(
                fields=["question", "text"], name="unique_choice_text_per_question"
            ),
            # 2. Ensures only ONE choice can be 'is_correct=True' per question.
            models.UniqueConstraint(
                fields=["question"],
                condition=models.Q(is_correct=True),
                name="unique_correct_choice_per_question",
            ),
        ]

    def __str__(self):
        return f"{self.text[:50]} ({'Correct' if self.is_correct else 'Incorrect'})"
