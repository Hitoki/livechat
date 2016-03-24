#!/usr/bin/env bash

cd //code

redis-server --daemonize yes

redis-cli PING

celery -A livechat.celery worker --loglevel=info

python livechat.py

/bin/bash