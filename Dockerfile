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

RUN apt-get update -y
RUN apt-get install -y redis-server

# Run commands

RUN chmod +x start.sh

ENTRYPOINT ["/code/start.sh"]

