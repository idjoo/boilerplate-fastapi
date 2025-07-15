FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install --assume-yes git

COPY uv.lock .

COPY pyproject.toml .

RUN uv sync --frozen --no-install-project --no-editable

COPY . /app

RUN uv sync --frozen --no-editable



FROM python:3.12-slim

WORKDIR /app

RUN useradd --uid 1000 --user-group --system app \
  && chown --recursive app:app /app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

USER app

CMD ["/app/.venv/bin/app"]
