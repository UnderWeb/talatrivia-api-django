# config/env.py
"""
Centralized environment loader for Talatrivia API.

Responsibilities:
- Read, validate, and type-cast environment variables.
- Provide immutable, typed dataclasses for Django settings consumption.
- Environment behavior is resolved by Django settings modules, not here.
- This module is intentionally environment-agnostic.
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional


# ======================================================
# Environment Metadata (non-behavioral)
# ======================================================
class Environment(str, Enum):
    """
    Supported runtime environments.

    This enum is intentionally not used for branching logic.
    Environment selection is handled by Django settings modules
    (config.settings.development / staging / production).
    """

    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


# ======================================================
# Helpers
# ======================================================
def _to_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "yes", "on"}


def _get(
    name: str,
    default=None,
    *,
    required: bool = False,
    cast: Optional[Callable] = None,
):
    """
    Retrieve and validate an environment variable.

    - No side effects
    - No environment-based decisions
    - Explicit failure on invalid configuration
    """
    raw = os.getenv(name, default)

    if required and (raw is None or raw == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")

    if cast is not None and raw is not None:
        try:
            return cast(raw)
        except Exception as exc:
            raise RuntimeError(
                f"Invalid value for environment variable {name}: {raw}"
            ) from exc

    return raw


# ======================================================
# Project
# ======================================================
@dataclass(frozen=True)
class ProjectConfig:
    NAME: str = _get("APP_NAME", required=True)
    PORT: int = _get("APP_PORT", default=8000, cast=int)
    SLUG: str = _get("PROJECT_SLUG", required=True)
    URL: str = _get("PROJECT_URL", required=True)
    EMAIL: str = _get("PROJECT_EMAIL", required=True)


# ======================================================
# Secrets
# ======================================================
@dataclass(frozen=True)
class SecretsConfig:
    SECRET_KEY: str = _get("SECRET_KEY", required=True)


# ======================================================
# Database
# ======================================================
@dataclass(frozen=True)
class DatabaseConfig:
    URL: str = _get("DATABASE_URL", required=True)


# ======================================================
# Redis
# ======================================================
@dataclass(frozen=True)
class RedisConfig:
    URL: str = _get("REDIS_CACHE_URL", required=True)


# ======================================================
# Logging
# ======================================================
@dataclass(frozen=True)
class LoggingConfig:
    LEVEL: str = _get("LOG_LEVEL", default="INFO")


# ======================================================
# Public, immutable config instances
# ======================================================
project = ProjectConfig()
secrets = SecretsConfig()
database = DatabaseConfig()
redis = RedisConfig()
logging = LoggingConfig()
