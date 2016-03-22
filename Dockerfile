FROM python:3.5

VOLUME ["/code"]
ADD . /code
WORKDIR /code

EXPOSE 5000
CMD ["python", "-m", "http.server", "5000"]