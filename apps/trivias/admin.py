# apps/trivias/admin.py
"""
Main admin entry point for the trivias app.
Imports specialized admin classes to register themwithin the Django Admin.
"""
from django.contrib import admin

from .admins.participation_admin import ParticipationAdmin  # noqa: F401
from .admins.trivia_admin import TriviaAdmin  # noqa: F401
from .models.trivia_question import TriviaQuestion  # noqa: F401

# Registering UserAnswer or TriviaQuestion explicitly if needed for standalone search
from .models.user_answer import UserAnswer


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """
    Standalone admin for UserAnswer to allow granular searches across
    all participations.
    """

    list_display = ("participation", "question", "is_correct", "created_at")
    list_filter = ("is_correct", "created_at")
    search_fields = ("participation__user__email", "question__text")
    readonly_fields = ("is_correct", "created_at")
