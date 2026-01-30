# apps/users/serializers/user_serializer.py
from rest_framework import serializers

from ..enums.user_role import UserRole
from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for full User data.
    Used for admin CRUD and internal operations.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "is_active",
            "password",
            "date_joined",
            "last_login",
        ]
        read_only_fields = ["id", "date_joined", "last_login"]
        extra_kwargs = {
            "email": {"help_text": "Unique email of the user."},
            "full_name": {"help_text": "Full name of the user."},
            "role": {"help_text": "Role of the user, from UserRole enum."},
            "is_active": {"help_text": "Indicates if the user is active."},
        }

    def validate_role(self, value):
        """
        Business Rule: Only admins can change user roles.
        """
        request = self.context.get("request")
        user = request.user if request else None

        if self.instance:
            if self.instance.role != value:
                if not (user and (user.is_staff or user.role == UserRole.ADMIN)):
                    raise serializers.ValidationError(
                        "You do not have permission to change the role."
                    )
        return value

    def create(self, validated_data):
        """Uses create_user to ensure password hashing on creation."""
        role = validated_data.get("role")
        if role == UserRole.ADMIN:
            validated_data["is_staff"] = True

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom update to handle password hashing and prevent plain text storage.
        """
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)
