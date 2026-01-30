# config/settings/development.py
"""
Development settings.

Local development configuration intended for engineers working on the
codebase.

Characteristics:
- DEBUG enabled
- Relaxed security settings
- Local or non-SSL database connections
- Explicit CORS allowances for frontend development
- Developer tooling enabled (e.g. debug toolbar, extensions)

This configuration must never be used in staging or production environments.
"""

from .base import *

# ======================================================
# DEBUG & SECURITY
# ======================================================
DEBUG = True

ALLOWED_HOSTS: list[str] = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
]


# ======================================================
# DATABASE
# ======================================================
DATABASES["default"].setdefault("OPTIONS", {})
DATABASES["default"]["OPTIONS"].update(
    {
        "connect_timeout": 10,
        "sslmode": "disable",
    }
)


# ======================================================
# CORS
# ======================================================
CORS_ALLOWED_ORIGINS: list[str] = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


# ======================================================
# CSRF
# ======================================================
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


# ======================================================
# DEVELOPMENT TOOLS
# ======================================================
INSTALLED_APPS += [
    "django_extensions",
]

INTERNAL_IPS = ["127.0.0.1"]

LOGGING["loggers"]["django.db.backends"] = {
    "handlers": ["console"],
    "level": "DEBUG",
    "propagate": False,
}
