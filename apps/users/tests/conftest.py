# apps/users/tests/conftest.py
"""
Pytest fixtures for the Users app.
Provides reusable instances and API clients for integration testing.
"""
import pytest
from rest_framework.test import APIClient

from apps.users.tests.factories import AdminFactory, PlayerFactory


@pytest.fixture
def api_client():
    """
    Returns a Rest Framework APIClient instance.
    """
    return APIClient()


@pytest.fixture
def user(db):
    """
    Standard player user fixture.
    """
    return PlayerFactory()


@pytest.fixture
def admin_user(db):
    """
    Administrator user fixture with staff and superuser privileges.
    """
    return AdminFactory()


@pytest.fixture
def auth_client(api_client, user):
    """
    Returns an APIClient authenticated as a standard player.
    """
    api_client.force_authenticate(user=user)
    return api_client
