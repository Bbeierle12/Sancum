#!/bin/sh
set -e

if [ "$SERVICE_TO_RUN" = "cme_service" ]; then
    exec uvicorn src.cme_service:app --host 0.0.0.0 --port 8000
elif [ "$SERVICE_TO_RUN" = "pivot_service" ]; then
    exec uvicorn src.pivot_service:app --host 0.0.0.0 --port 8001
else
    echo "Error: SERVICE_TO_RUN environment variable not set or invalid."
    exit 1
fi
