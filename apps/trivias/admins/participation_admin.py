# apps/trivias/admins/participation_admin.py
from django.contrib import admin

from ..models.participation import Participation
from ..models.user_answer import UserAnswer


class UserAnswerInline(admin.TabularInline):
    """
    Read-only inline to view a user's answers within their participation session.
    """

    model = UserAnswer
    readonly_fields = ("question", "chosen_choice", "is_correct", "created_at")
    extra = 0
    can_delete = False


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Participation model.
    Tracks user sessions, scores, and specific answers per trivia.
    """

    list_display = (
        "user",
        "trivia",
        "total_score",
        "start_time",
        "end_time",
        "is_finished",
    )
    list_filter = ("trivia", "end_time")
    search_fields = ("user__email", "trivia__name")
    readonly_fields = ("start_time", "created_at", "updated_at")
    inlines = [UserAnswerInline]

    def is_finished(self, obj):
        """
        Displays a boolean status based on the existence of end_time.
        """
        return obj.is_finished

    is_finished.boolean = True
