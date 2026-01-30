# apps/conftest.py
import pytest

from apps.users.tests.factories import UserFactory


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def admin_user():
    return UserFactory(is_staff=True, is_superuser=True)
