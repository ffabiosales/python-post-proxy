FROM python:3.10

ADD requirements.txt /tmp/
RUN mkdir /app && pip install -r /tmp/requirements.txt
WORKDIR /app