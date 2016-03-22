#Set the base image to use to python 3.5
FROM python:3.5

# Set the file maintainer
MAINTAINER Vitaliy Romanuik

# Set env
ENV livechat 1

# Create application subdirectories
RUN mkdir /livechat
WORKDIR /livechat
RUN cd /livechat
ADD . /livechat/


# Install Python dependencies
ADD requirements.txt /livechat/
RUN pip install -r requirements.txt

# Port to expose
EXPOSE 5000

# Run django commands
CMD python livechat.py