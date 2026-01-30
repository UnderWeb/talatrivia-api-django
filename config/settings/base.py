# config/settings/base.py
"""
Django settings for Talatrivia API project.
Base settings shared across all environments.

This file:
- Imports all configuration from config.env
- Contains environment-agnostic defaults only
- Does not read os.getenv directly (single source of truth = env.py)
"""
from datetime import timedelta
from pathlib import Path

import dj_database_url
from corsheaders.defaults import default_headers, default_methods

from .. import env

# ======================================================
# PATHS
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ======================================================
# CORE DJANGO
# ======================================================
SECRET_KEY = env.secrets.SECRET_KEY


# ======================================================
# APPLICATIONS
# ======================================================
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "django_filters",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
]

LOCAL_APPS = [
    "apps.core",
    "apps.users",
    "apps.questions",
    "apps.trivias",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ======================================================
# MIDDLEWARE
# ======================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ======================================================
# URLS / WSGI / ASGI
# ======================================================
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# ======================================================
# DATABASES
# ======================================================
DATABASES = {
    "default": dj_database_url.parse(
        env.database.URL,
        conn_max_age=600,
    )
}


# ======================================================
# CACHE
# ======================================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.redis.URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 300,
        "KEY_PREFIX": env.project.SLUG,
    }
}


# ======================================================
# USER MODEL
# ======================================================
AUTH_USER_MODEL = "users.User"


# ======================================================
# DEFAULT PRIMARY KEY
# ======================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ======================================================
# ALLOWED HOSTS
# ======================================================
ALLOWED_HOSTS: list[str] = []


# ======================================================
# TEMPLATES
# ======================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ======================================================
# PASSWORD VALIDATION
# ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ======================================================
# INTERNATIONALIZATION
# ======================================================
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ("en", "English"),
    ("es", "Spanish"),
]

LOCALE_PATHS = [
    Path.joinpath(BASE_DIR, "locale"),
]

FIXTURE_DIRS = ["fixtures"]
APPEND_SLASH = False


# ======================================================
# AUTH / JWT
# ======================================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env.secrets.SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_TYPE_CLAIM": "token_type",
}


# ======================================================
# DJANGO REST FRAMEWORK
# ======================================================
REST_FRAMEWORK = {
    # ------------------------------------------------------------------
    # AUTH
    # ------------------------------------------------------------------
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    # ------------------------------------------------------------------
    # SCHEMA / DOCUMENTATION
    # ------------------------------------------------------------------
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # ------------------------------------------------------------------
    # FILTERING / SEARCH / ORDERING
    # ------------------------------------------------------------------
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    # ------------------------------------------------------------------
    # THROTTLING
    # ------------------------------------------------------------------
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "user": "1000/hour",
        "anon": "100/hour",
    },
    # ------------------------------------------------------------------
    # VERSIONING
    # ------------------------------------------------------------------
    "DEFAULT_VERSIONING_CLASS": ("rest_framework.versioning.NamespaceVersioning"),
}


# ======================================================
# DRF SPECTACULAR (SWAGGER/OPENAPI)
# ======================================================
SPECTACULAR_SETTINGS = {
    "TITLE": env.project.NAME,
    "DESCRIPTION": f"API Documentation for {env.project.NAME}",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "CONTACT": {
        "name": "UnderWeb",
        "email": env.project.EMAIL,
        "url": env.project.URL,
    },
    "SECURITY": [
        {"Bearer": []},
    ],
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}


# ======================================================
# CORS / CSRF
# ======================================================
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = list(default_methods)
CORS_ALLOW_HEADERS = list(default_headers) + [
    "accept-language",
    "access-token",
    "referer",
    "sec-fetch-site",
]


# ======================================================
# LOGGING
# ======================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": env.logging.LEVEL,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.logging.LEVEL,
    },
    "loggers": {
        "config": {
            "handlers": ["console"],
            "level": env.logging.LEVEL,
            "propagate": False,
        },
        "apps.core": {
            "level": env.logging.LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "apps.users": {
            "level": env.logging.LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "apps.questions": {
            "level": env.logging.LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        "apps.trivias": {
            "level": env.logging.LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
    },
}

# ======================================================
# STATIC FILES (CSS, JavaScript, Images)
# ======================================================
# URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = "static/"

# The absolute path to the directory where collectstatic will collect static files.
# In Docker, this is usually a shared volume.
STATIC_ROOT = BASE_DIR / "staticfiles"

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
