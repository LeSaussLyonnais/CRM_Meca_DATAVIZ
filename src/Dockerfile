FROM python:3.10-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev libffi-dev
#RUN apk update && apk add build-base

RUN mkdir /codes/
WORKDIR /codes

COPY requirements.txt /codes
RUN pip install gunicorn uvicorn[standard]
RUN pip install -r requirements.txt

COPY ProjetDjango1 ProjetDjango1
COPY BlogApp BlogApp
COPY Dockerfile Dockerfile
COPY manage.py manage.py
COPY data data
COPY gunicorn.app.conf.py gunicorn.app.conf.py
COPY gunicorn.channel.conf.py gunicorn.channel.conf.py
#COPY . .
#COPY db.sqlite3 db.sqlite3


RUN python3 manage.py collectstatic --no-input
#RUN celery -A ProjetDjango1 worker --beat -l info

EXPOSE 8000