# apps/questions/enums/difficulty_level.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class DifficultyLevel(models.TextChoices):
    """Difficulty levels for questions."""

    EASY = "EASY", _("Easy")
    MEDIUM = "MEDIUM", _("Medium")
    HARD = "HARD", _("Hard")
