# apps/users/urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views.auth_viewset import AuthViewSet
from apps.users.views.user_viewset import UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path(
                    "login/", AuthViewSet.as_view({"post": "login"}), name="auth-login"
                ),
                path(
                    "logout/",
                    AuthViewSet.as_view({"post": "logout"}),
                    name="auth-logout",
                ),
                path("me/", AuthViewSet.as_view({"get": "me"}), name="auth-me"),
                path(
                    "refresh/",
                    AuthViewSet.as_view({"post": "refresh"}),
                    name="auth-refresh",
                ),
            ]
        ),
    ),
    path("", include(router.urls)),
]
