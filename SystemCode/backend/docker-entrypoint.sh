#!/usr/bin/env sh
set -e

cd /app

# 2. hand off to uvicorn with debugging enabled (also exposes debug-level logs)
export PYTHONUNBUFFERED=1
export PYTHONPATH=/app

# Set an environment variable for debugging if desired (optional)
export LOG_LEVEL=debug

# You can set additional debug options or envs here, e.g.:
# export SOME_CUSTOM_DEBUG_SETTING=1

# Run uvicorn with debug logging
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug