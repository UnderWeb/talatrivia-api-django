# apps/users/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..enums.user_role import UserRole
from ..managers.user_manager import UserManager


class User(AbstractUser):
    """
    Custom User model for Talatrivia.
    Identity is based on email, and roles are driven by UserRole enum.
    """

    username = None
    first_name = None
    last_name = None

    # Identity fields
    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=255)

    # Business logic fields
    role = models.CharField(
        _("role"),
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.PLAYER,
        db_index=True,
        help_text=_("Role of the user in the system, determines access level."),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-date_joined"]

    @property
    def short_name(self):
        """Returns the first part of the full name."""
        return self.full_name.split()[0] if self.full_name else self.email

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
