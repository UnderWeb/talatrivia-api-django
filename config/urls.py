# config/urls.py
"""
Root URL configuration for Talatrivia API.

API versioning: v1 namespace with DRF Spectacular documentation.
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.core.views import HealthCheckView

# API V1
api_v1_patterns = [
    path("", include("apps.users.urls")),
    path("", include("apps.questions.urls")),
    path("", include("apps.trivias.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health-check"),
    # --- DOCUMENTATION API V1 ---
    path(
        "api/v1/schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema-v1"
    ),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema-v1"),
        name="redoc",
    ),
    path("api/v1/", include((api_v1_patterns, "v1"))),
]
