# apps/users/views/auth_viewset.py
import logging

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from ..serializers.login_serializer import LoginSerializer
from ..serializers.me_serializer import MeSerializer
from ..serializers.token_serializer import (
    LogoutSerializer,
    RefreshSerializer,
    TokenPairSerializer,
)
from ..services.auth_service import AuthService

logger = logging.getLogger(__name__)


class AuthViewSet(viewsets.ViewSet):
    """
    Authentication ViewSet handling JWT lifecycle.
    Includes login, token refresh, logout, and current user profile.
    """

    permission_classes_by_action = {
        "login": [AllowAny],
        "refresh": [AllowAny],
        "logout": [IsAuthenticated],
        "me": [IsAuthenticated],
    }

    def get_permissions(self):
        """
        Dynamically assigns permissions based on the action name.
        Defaults to IsAuthenticated if action is not mapped.
        """
        permissions = self.permission_classes_by_action.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permissions]

    @extend_schema(request=LoginSerializer, responses={200: TokenPairSerializer})
    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request):
        """
        Verifies credentials and issues a fresh JWT pair.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request=request,
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )
        if not user or not user.is_active:
            logger.warning(
                f"Unauthorized login attempt: {serializer.validated_data['email']}"
            )
            raise AuthenticationFailed("Invalid credentials or inactive account")

        tokens = AuthService.generate_tokens_for_user(user)
        logger.info(f"User login successful: {user.email}")
        return Response(tokens, status=status.HTTP_200_OK)

    @extend_schema(request=RefreshSerializer, responses={200: TokenPairSerializer})
    @action(detail=False, methods=["post"], url_path="refresh")
    def refresh(self, request):
        """
        Renews an access token using a valid refresh token.
        """
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            tokens = AuthService.refresh_tokens(serializer.validated_data["refresh"])
            return Response(tokens, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(request=LogoutSerializer, responses={204: None})
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        """
        Logout a user by blacklisting their refresh token.
        """
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            AuthService.logout(serializer.validated_data["refresh"])
            logger.info(f"User {request.user.email} logged out.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Logout error for {request.user.email}: {str(e)}")
            return Response(
                {"detail": "Logout failed"}, status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(responses={200: MeSerializer})
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Return current authenticated user's data.
        """
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
