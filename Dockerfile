#Set the base image to use to python 3.5
FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/

EXPOSE 5000

# Install the Redis server
#RUN wget http://download.redis.io/redis-stable.tar.gz
#RUN tar xvzf redis-stable.tar.gz
#WORKDIR redis-stable
#RUN make
#WORKDIR /code

RUN apt-get update -y
RUN apt-get install -y redis-server

# Run commands

# OK, 502
# service redis-server start

# OK, 502
# redis-server --daemonize yes

# redis /usr/bin/redis-server
# redis-server /etc/redis/redis.conf

EXPOSE 6379

CMD service redis-server start && celery -A livechat.celery worker --loglevel=info && python livechat.py

