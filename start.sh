#!/usr/bin/env bash

cd //code

redis-server --daemonize yes

#python run.py

gunicorn livechat:app --config gunicorn/config --daemon

#celery -A livechat.tasks.celery worker --loglevel=info
su -c "celery -A livechat.tasks.celery worker -l info" celeryuser

/bin/bash