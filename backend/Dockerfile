# ================= Stage 1. Builder =================
FROM python:3.12-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Change dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy all project files
COPY pyproject.toml uv.lock ./
COPY src ./src

# Install the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable


# ================= Stage 2. Runtime =================
FROM python:3.12-slim

# Change the working directory to the `app` directory
WORKDIR /app

# Create non-root user
RUN groupadd -r dashboard && \
    useradd -r -g dashboard -u 1000 dashboard-user && \
    chown -R dashboard-user:dashboard /app

# Copy the virtual environment from builder
COPY --from=builder --chown=dashboard-user:dashboard /app/.venv /app/.venv

# Copy source code from builder
COPY --from=builder --chown=dashboard-user:dashboard /app/src /app/src

# Copy project metadata
COPY --chown=dashboard-user:dashboard pyproject.toml ./

# Copy alembic configuration and migration scripts
COPY --chown=dashboard-user:dashboard alembic.ini ./
COPY --chown=dashboard-user:dashboard migration ./migration
COPY --chown=dashboard-user:dashboard scripts/entrypoint.sh ./

# Add .venv/bin to PATH so we can run uvicorn
ENV PATH="/app/.venv/bin:$PATH"

# Set environment variables
ENV PYTHONPATH="/app/src:$PYTHONPATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER dashboard-user

# Expose application port
EXPOSE 8000

# Run the apllication
CMD ["sh", "entrypoint.sh"]