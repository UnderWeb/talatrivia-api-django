# apps/trivias/models/participation.py
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.users.models.user import User

from .trivia import Trivia


class Participation(models.Model):
    """
    Represents a user's participation in a specific trivia.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="participations",
        verbose_name=_("User"),
    )
    trivia = models.ForeignKey(
        Trivia,
        on_delete=models.CASCADE,
        related_name="participations",
        verbose_name=_("Trivia"),
    )
    start_time = models.DateTimeField(
        default=timezone.now, verbose_name=_("Start Time")
    )
    end_time = models.DateTimeField(verbose_name=_("End Time"), null=True, blank=True)
    total_score = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Total Score"),
        help_text=_("The total score obtained in this participation."),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Participation")
        verbose_name_plural = _("Participations")
        ordering = ["-start_time"]
        unique_together = [["user", "trivia"]]
        indexes = [
            models.Index(fields=["trivia", "total_score"]),
        ]

    def __str__(self):
        return f"{self.user.email} in {self.trivia.name} ({self.total_score})"

    @property
    def is_finished(self) -> bool:
        return self.end_time is not None

    @property
    def duration_seconds(self) -> float:
        """Calculates duration in seconds for ranking purposes."""
        if self.end_time:
            delta = self.end_time - self.start_time
            return delta.total_seconds()
        return 0.0
