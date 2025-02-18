#!/bin/sh
# Exit script on error or uninitialized variables
set -o errexit
set -o nounset

: "${CELERY_GRADING_QUEUE:=grading}"
: "${CELERY_LIFECYCLE_EVENTS_QUEUE:=lifecycle_events}"
: "${CELERY_DEFAULT_QUEUE:=default}"

# Ensure logs appear in Docker by running Celery in the foreground
celery -A src.worker.celery_app multi start 7 \
    --loglevel=INFO \
    --pidfile=/var/run/celery/%n.pid \
    --logfile=/codegrade_backend/logs/%n.log \
    -Q:1-4 "${CELERY_GRADING_QUEUE}" \
    -Q:5,6 "${CELERY_LIFECYCLE_EVENTS_QUEUE}" \
    -Q "${CELERY_DEFAULT_QUEUE}"


# Keep the container running
tail -f /codegrade_backend/logs/*.log
