# config/settings/production.py
"""
Production settings.

This file contains the final, security-hardened configuration used in live
environments.

Characteristics:
- DEBUG disabled
- Strict SSL and HSTS enforcement
- Minimal and explicit allowed hosts and origins
- Verified database connections
- Least-privilege configuration

Any change to this file must be reviewed carefully, as it directly impacts
live users and data.
"""

from .base import *

# ======================================================
# SECURITY
# ======================================================
DEBUG = False

ALLOWED_HOSTS: list[str] = [
    "talatrivia.com",
    ".talatrivia.com",
]

# --- HTTPS / Cookies ---
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Lax"

# --- HSTS ---
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# --- Reverse proxy / load balancer ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# --- Security headers ---
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True  # Legacy, harmless, kept for compatibility
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# ======================================================
# DATABASE
# ======================================================
DATABASES["default"].setdefault("OPTIONS", {})
DATABASES["default"]["OPTIONS"].update(
    {
        "connect_timeout": 10,
        "sslmode": "verify-full",
        "sslrootcert": "/etc/ssl/certs/rds-ca-bundle.pem",
    }
)


# ======================================================
# CORS
# ======================================================
CORS_ALLOWED_ORIGINS: list[str] = [
    "https://talatrivia.com",
    "https://app.talatrivia.com",
]


# ======================================================
# CSRF
# ======================================================
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


# ======================================================
# LOGGING
# ======================================================
LOGGING["root"]["level"] = "INFO"
