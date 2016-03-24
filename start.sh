#!/usr/bin/env bash

cd //code

redis-server --daemonize yes

python livechat.py

celery -A livechat.celery worker --loglevel=info

/bin/bash