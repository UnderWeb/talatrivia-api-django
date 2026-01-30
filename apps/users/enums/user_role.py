# apps/users/enums/user_role.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    PLAYER = "PLAYER", _("Player")
