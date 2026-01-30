# apps/users/tests/test_models.py
"""
Unit tests for the User model and its Manager.
Covers creation, string representation, properties, and custom manager logic.
"""
import pytest
from django.db import IntegrityError

from apps.users.enums.user_role import UserRole
from apps.users.models.user import User
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserModel:

    def test_user_creation(self):
        """Tests that the factory and model basic creation work."""
        user = UserFactory()
        assert isinstance(user, User)
        assert user.role == UserRole.PLAYER
        assert user.is_active is True

    def test_user_str_method(self):
        """Verifies the string representation matches the expected format."""
        user = UserFactory(full_name="Patrick Donald", email="pdonald@example.com")
        assert str(user) == "Patrick Donald <pdonald@example.com>"

    def test_user_short_name_logic(self):
        """Checks the short_name property with multiple and single names."""
        user_mult = UserFactory(full_name="Zoila Cerda")
        user_single = UserFactory(full_name="Bob")

        assert user_mult.short_name == "Zoila"
        assert user_single.short_name == "Bob"

    def test_email_uniqueness_constraint(self):
        """Ensures that the database enforces unique emails."""
        User.objects.create(email="duplicate@example.com", full_name="User 1")
        with pytest.raises(IntegrityError):
            User.objects.create(email="duplicate@example.com", full_name="User 2")

    def test_create_superuser_manager(self):
        """
        Verifies that the UserManager correctly sets admin flags and roles.
        This is a critical security test.
        """
        admin = User.objects.create_superuser(
            email="admin@talatrivia.cl",
            password="secure_password",
            full_name="Main Admin",
        )
        assert admin.is_superuser is True
        assert admin.is_staff is True
        assert admin.role == UserRole.ADMIN
