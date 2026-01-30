# apps/trivias/admins/trivia_admin.py
from django.contrib import admin

from ..models.trivia import Trivia
from ..models.trivia_question import TriviaQuestion


class TriviaQuestionInline(admin.TabularInline):
    """
    Inline admin to manage the relationship between Trivias and Questions.
    Allows defining the order of questions within the trivia.
    """

    model = TriviaQuestion
    extra = 1
    autocomplete_fields = ["question"]


@admin.register(Trivia)
class TriviaAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Trivia model.
    Organizes the collection of questions associated with each game.
    """

    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name", "description")
    inlines = [TriviaQuestionInline]
