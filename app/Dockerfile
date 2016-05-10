FROM python:3-alpine

COPY requirements.txt /tmp/requirements.txt
COPY setup.sh /tmp/setup.sh

RUN apk update && \
    apk add \
            gcc \
            musl-dev \
            postgresql-contrib \
            postgresql-dev \
            && \
    pip install --upgrade -r /tmp/requirements.txt
