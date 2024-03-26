FROM python:3.10-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev libffi-dev
#RUN apk update && apk add build-base

RUN mkdir /ProjetDjango1
WORKDIR /ProjetDjango1

COPY requirements.txt /ProjetDjango1

RUN pip install -r requirements.txt

COPY ProjetDjango1 ProjetDjango1
COPY BlogApp BlogApp
COPY Dockerfile Dockerfile
COPY manage.py manage.py
COPY db.sqlite3 db.sqlite3


RUN python3 manage.py collectstatic --no-input

EXPOSE 8000
