# ==============================================================
# BASE STAGE
# ==============================================================
# Foundation layer with system dependencies and Python environment.
FROM python:3.10-slim AS base

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.0.0 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

# Install system dependencies required for building Python packages and runtime tools.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gettext \
    netcat-openbsd \
    curl && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry for dependency management.
RUN pip install "poetry==$POETRY_VERSION"

# ==============================================================
# DEPENDENCIES STAGE
# ==============================================================
# Installs Python dependencies in a virtual environment layer.
# This layer is cached unless pyproject.toml or poetry.lock changes.
FROM base AS dependencies

RUN python -m venv $VIRTUAL_ENV

COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --without dev --no-root

# ==============================================================
# DEVELOPMENT STAGE
# ==============================================================
# Optimized for local development with hot-reload, debug tools, and dev dependencies.
FROM dependencies AS development

ENV PATH="/opt/venv/bin:$PATH"

RUN poetry install --no-interaction --no-ansi --with dev

COPY . .
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=config.settings.development \
    DEBUG=1 \
    PORT=8000 \
    PYTHONPATH="/usr/src/app:$PYTHONPATH"

EXPOSE ${PORT}

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ==============================================================
# PRODUCTION STAGE
# ==============================================================
# Hardened runtime for production workloads with Gunicorn WSGI server.
# Runs as non-root user with healthchecks and optimized worker configuration.
FROM dependencies AS production

ENV PATH="/opt/venv/bin:$PATH"

# Create non-root application user and required directories for static files.
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -s /bin/false appuser && \
    mkdir -p /usr/src/app/static && \
    chown -R appuser:appgroup /usr/src/app

COPY --chown=appuser:appgroup . .
COPY --chown=appuser:appgroup docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

ENV DJANGO_SETTINGS_MODULE=config.settings.production \
    DEBUG=False \
    PORT=8000 \
    PYTHONPATH="/usr/src/app:$PYTHONPATH"

EXPOSE ${PORT}

# Healthcheck ensures the container is considered healthy only when the Django app responds.
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health/ || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD gunicorn config.wsgi:application \
    --bind 0.0.0.0:${PORT} \
    --workers ${GUNICORN_WORKERS:-3} \
    --threads ${GUNICORN_THREADS:-2} \
    --timeout ${GUNICORN_TIMEOUT:-60} \
    --worker-tmp-dir /dev/shm \
    --access-logfile - \
    --error-logfile -
