#!/bin/sh

uv run python3 manage.py collectstatic --no-input
uv run python3 manage.py migrate

exec "$@"
