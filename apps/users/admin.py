# apps/users/admin.py
"""
Main admin entry point for the users app.
Exposes the customized UserAdmin for the identity management.
"""

from django.contrib import admin  # noqa: F401

from .admins.user_admin import UserAdmin  # noqa: F401
