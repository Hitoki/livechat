#!/usr/bin/env bash

cd //code

redis-server --daemonize yes

#python run.py

gunicorn livechat:app --config gunicorn/config --daemon

celery -A livechat.tasks.celery worker --loglevel=info

/bin/bash