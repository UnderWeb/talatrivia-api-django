# apps/questions/admins/choice_admin.py
from django.contrib import admin

from ..models.choice import Choice


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Choice model.
    Used for granular management and searching of specific answer options.
    """

    list_display = ("text", "question", "is_correct")
    list_filter = ("is_correct", "question__difficulty")
    search_fields = ("text", "question__text")
    autocomplete_fields = ["question"]
