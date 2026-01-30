# apps/questions/admins/question_admin.py
from django.contrib import admin

from ..models.choice import Choice
from ..models.question import Question


class ChoiceInline(admin.TabularInline):
    """
    Inline admin configuration for Choice model.
    Allows managing answer options directly from the Question detail page.
    """

    model = Choice
    extra = 3
    fields = ("text", "is_correct")
    min_num = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.
    Provides filtering by difficulty and integrated choice management via inlines.
    """

    list_display = ("text_short", "difficulty", "created_at")
    list_filter = ("difficulty", "created_at")
    search_fields = ("text",)
    inlines = [ChoiceInline]

    def text_short(self, obj):
        """
        Returns a truncated version of the question text for list display.
        """
        return obj.text[:75] + "..." if len(obj.text) > 75 else obj.text

    text_short.short_description = "Question Text"
