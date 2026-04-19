FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

COPY alembic.ini ./
COPY src ./src
COPY tests ./tests

CMD ["pytest"]
