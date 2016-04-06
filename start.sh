#!/usr/bin/env bash

cd //code

redis-server --daemonize yes

gunicorn livechat:app --config gunicorn/config --daemon

su -c "celery -A livechat.tasks.celery worker -l info" celeryuser

/bin/bash