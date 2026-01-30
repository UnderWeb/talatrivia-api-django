# apps/users/admins/user_admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from ..models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    Customized to handle email-based identity and specific business roles.
    """

    list_display = (
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "full_name")
    ordering = ("-date_joined",)

    # Customizing fieldsets because we removed username, first_name, and last_name
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "role")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password"),
            },
        ),
    )
