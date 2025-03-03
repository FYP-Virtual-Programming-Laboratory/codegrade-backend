#!/bin/sh
# Exit script on error or uninitialized variables
set -o errexit
set -o nounset

: "${CELERY_GRADING_QUEUE:=grading}"
: "${CELERY_DEFAULT_QUEUE:=default}"

# Ensure logs appear in Docker by running Celery in the foreground
celery -A src.worker.celery_app multi start 2 \
    --loglevel=INFO \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/codegrade_backend/logs/%n.log \
    -Q:1 "${CELERY_GRADING_QUEUE}" \
    -Q "${CELERY_DEFAULT_QUEUE}"


# Keep the container running
tail -f /codegrade_backend/logs/*.log
