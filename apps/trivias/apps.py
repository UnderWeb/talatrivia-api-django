# apps/trivias/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TriviasConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.trivias"
    verbose_name = _("Trivias")
