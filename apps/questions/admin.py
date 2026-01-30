# apps/questions/admin.py
"""
Main admin module for the questions app.
Imports and exposes the specialized admin classes to the Django admin site.
"""

from django.contrib import admin  # noqa: F401

from .admins.choice_admin import ChoiceAdmin  # noqa: F401
from .admins.question_admin import QuestionAdmin  # noqa: F401
