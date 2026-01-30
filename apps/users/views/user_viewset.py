# apps/users/views/user_viewset.py
import logging

from rest_framework import permissions, viewsets

from ..enums.user_role import UserRole
from ..models.user import User
from ..serializers.user_serializer import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user instances.

    Provides standard CRUD actions while ensuring strict data isolation
    between regular players and administrative staff.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        Allows any user to register, but requires authentication for other actions.
        """
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]

        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Filters the queryset based on user roles.
        Administrators can access all records, while regular players
        are restricted to their own profile.
        """
        user = self.request.user
        if user.is_authenticated and (user.is_staff or user.role == UserRole.ADMIN):
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

    def perform_create(self, serializer):
        """
        Logs the successful registration of a new user for audit purposes.
        """
        user = serializer.save()
        logger.info(f"User created: {user.email} with role: {user.role}")

    def perform_destroy(self, instance):
        """
        Logs account deletion events, which is critical for security auditing.
        """
        user_email = instance.email
        logger.warning(f"User deleted: {user_email} by {self.request.user.email}")
        instance.delete()
