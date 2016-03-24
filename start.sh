#!/usr/bin/env bash

cd //code

redis-server --daemonize yes
#service redis-server restart

#celery -A livechat.celery worker --loglevel=info

huey_consumer.py livechat.huey -k process -w 64

python livechat.py

/bin/bash