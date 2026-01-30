# apps/users/managers/user_manager.py
from django.contrib.auth.models import BaseUserManager

from ..enums.user_role import UserRole


class UserManager(BaseUserManager):
    """
    Custom manager for User model where email is the unique identifier.
    """

    def _create_user(self, email, password, **extra_fields):
        """
        Internal helper to handle core user creation logic.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Public method to create a standard Player.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("role", UserRole.PLAYER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Public method to create a Superuser with Admin role.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", UserRole.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
