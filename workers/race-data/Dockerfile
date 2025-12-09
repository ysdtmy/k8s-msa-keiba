FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-install-project --no-dev

COPY . .

ENV PATH="/app/.venv/bin:$PATH"
ENV APP_PORT=8081

CMD ["fastapi", "run", "main.py", "--port", "8081"]
