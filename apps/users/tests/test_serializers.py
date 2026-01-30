# apps/users/tests/test_serializers.py
"""
Unit tests for User serializers.
Validates data integrity, security constraints, and field mapping.
"""
import pytest

from apps.users.serializers.user_serializer import UserSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """
    Test suite for UserSerializer logic and constraints.
    """

    def test_user_serialization_output(self, user):
        """
        Test that the serializer output contains expected fields
        and excludes sensitive data.
        Expected: Correct mapping of email, name, and role,
        with no password field present.
        """
        serializer = UserSerializer(instance=user)
        data = serializer.data

        # Check expected fields
        assert data["email"] == user.email
        assert data["full_name"] == user.full_name
        assert data["role"] == user.role

        # Security check: Password should NEVER be in the output
        assert "password" not in data

    def test_read_only_fields_constraint(self, user):
        """
        Test that critical system fields remain unchanged when included in
        an update request.
        Expected: User ID and joined date values are not modified after saving.
        """
        original_id = user.id
        original_date = user.date_joined

        update_payload = {"id": 9999, "date_joined": "2026-01-30T23:59:59Z"}

        serializer = UserSerializer(instance=user, data=update_payload, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # The values should remain unchanged
        user.refresh_from_db()
        assert user.id == original_id
        assert user.date_joined == original_date

    def test_invalid_email_validation(self):
        """
        Test that the serializer identifies and rejects malformed email addresses.
        Expected: is_valid() returns False and includes an error for the email field.
        """
        invalid_data = {
            "email": "not-an-email-format",
            "full_name": "Patrick Donald",
            "role": "PLAYER",
        }
        serializer = UserSerializer(data=invalid_data)

        assert serializer.is_valid() is False
        assert "email" in serializer.errors
