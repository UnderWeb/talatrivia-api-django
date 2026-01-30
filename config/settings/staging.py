# config/settings/staging.py
"""
Staging settings.

This environment mirrors production as closely as possible while allowing
increased observability for validation, QA, and release verification.

Characteristics:
- DEBUG disabled
- Full security headers enabled
- SSL enforced
- Real infrastructure (DB, cache, storage)
- Logging more verbose than production

No development-only tooling should be enabled here.
"""

from .base import *

# ======================================================
# SECURITY
# ======================================================
DEBUG = False

ALLOWED_HOSTS: list[str] = [
    "staging.talatrivia.com",
    "testing.talatrivia.com",
    "sandbox.talatrivia.com",
]

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

USE_X_FORWARDED_HOST = True


# ======================================================
# DATABASE
# ======================================================
DATABASES["default"].setdefault("OPTIONS", {})
DATABASES["default"]["OPTIONS"].update(
    {
        "connect_timeout": 10,
        "sslmode": "require",
        "sslrootcert": "/etc/ssl/certs/rds-ca-bundle.pem",
    }
)


# ======================================================
# CORS
# ======================================================
CORS_REPLACE_HTTPS_REFERER = True

CORS_ALLOWED_ORIGINS: list[str] = [
    "https://staging.talatrivia.com",
    "https://testing.talatrivia.com",
    "https://sandbox.talatrivia.com",
    "https://app-staging.talatrivia.com",
]


# ======================================================
# CSRF
# ======================================================
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS
