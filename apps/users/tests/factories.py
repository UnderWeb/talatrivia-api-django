# apps/users/tests/factories.py
"""
Factories for the Users app.
Includes UserFactory to generate test users with different roles and states.
"""
import factory
from django.contrib.auth import get_user_model

from apps.users.enums.user_role import UserRole

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for the Custom User model.
    By default, creates a verified PLAYER.
    """

    class Meta:
        model = User
        # Important: this avoids duplicate users if tests are poorly isolated
        django_get_or_create = ("email",)
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker("name")
    role = UserRole.PLAYER
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or "password123"
        self.set_password(password)
        if create:
            self.save()


class AdminFactory(UserFactory):
    """Specialized factory for administrator users."""

    role = UserRole.ADMIN
    is_staff = True
    is_superuser = True


class PlayerFactory(UserFactory):
    """Specialized factory for standard player users."""

    role = UserRole.PLAYER
