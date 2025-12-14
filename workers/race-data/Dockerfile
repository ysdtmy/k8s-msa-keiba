# Builder stage
FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies
# Note: uv sync --frozen needs uv.lock to exist
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Runner stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the environment from the builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy the application code
COPY . .

# Change ownership of the application code
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

ENV APP_PORT=8081

CMD ["fastapi", "run", "main.py", "--port", "8081"]
