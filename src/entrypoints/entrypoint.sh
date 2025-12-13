#!/bin/bash

uv run python3 manage.py migrate

exec "$@"
