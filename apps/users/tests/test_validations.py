# apps/users/tests/test_validations.py
"""
Validation tests for the User model.
Covers database constraints, required fields, and data integrity.
"""
import pytest
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from apps.users.models.user import User
from apps.users.serializers.user_serializer import UserSerializer
from apps.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestUserValidations:
    """
    Test suite for hard constraints and data validation rules.
    """

    def test_unique_email_constraint(self):
        """
        Test that the system prevents creating two users with the same email address.
        Expected: DRFValidationError raised by the serializer due to unique constraint.
        """
        email = "duplicate@example.com"
        User.objects.create(email=email, full_name="User 1")

        data = {"email": email, "full_name": "User 2", "password": "password123"}
        serializer = UserSerializer(data=data)

        with pytest.raises(DRFValidationError) as excinfo:
            serializer.is_valid(raise_exception=True)
        assert "email" in excinfo.value.detail

    def test_full_name_max_length(self):
        """
        Test that the full_name field enforces its maximum character limit.
        Expected: ValidationError raised during model full_clean when
        length exceeds 255.
        """
        long_name = "A" * 256
        user = UserFactory.build(full_name=long_name)

        with pytest.raises(ValidationError):
            user.full_clean()

    def test_invalid_email_format_at_model_level(self):
        """
        Test that the model layer rejects strings that do not follow
        a valid email format.
        Expected: ValidationError raised by Django's EmailField validatorduring clean.
        """
        user = UserFactory.build(email="not-an-email")

        with pytest.raises(ValidationError):
            user.full_clean()

    def test_role_choices_validation(self):
        """
        Test that the role field only accepts values defined in the
        UserRole enumeration.
        Expected: ValidationError raised during model cleaning for unauthorized
        role strings.
        """
        # We use build() to avoid saving and trigger manual validation
        user = UserFactory.build(role="INVALID_ROLE")

        with pytest.raises(ValidationError):
            user.full_clean()
