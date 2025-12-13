FROM python:3.11-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi \
    && useradd --no-log-init --create-home --shell /bin/bash --uid ${APP_USER_ID} app

USER app

WORKDIR /app

COPY --chown=app:app pyproject.toml uv.lock README.md ./
COPY --chown=app:app src/ /app/src/

RUN uv sync --group dev --no-cache

WORKDIR /app/src/

ENTRYPOINT ["/app/src/entrypoints/entrypoint.sh"]
