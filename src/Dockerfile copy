FROM python:3.10-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev libffi-dev
RUN apk update && \
    apk add unixodbc unixodbc-dev && \
    rm -rf /var/cache/apk/*
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
#COPY data data
COPY gunicorn.app.conf.py gunicorn.app.conf.py
COPY gunicorn.channel.conf.py gunicorn.channel.conf.py
#COPY ProjetDjango1/ODBCwin32 ODBCwin32
#COPY ProjetDjango1/ODBCwin64 ODBCwin64
COPY ODBC_Linux ODBC_Linux
#COPY . .
#COPY db.sqlite3 db.sqlite3

# Création ou modification du fichier odbc.ini avec les configurations HFSQL
RUN echo "[HFSQL_ODBC] \
my_hfsql_db = HFSQL_ODBC \
[my_hfsql_db] \
Driver = HFSQL \
ServerName = 192.168.0.21 \
Port = 4900 \
Database = BAC_A_SABLE \
UID = admin \
PWD = Clip_SERENA" > /etc/odbc.ini

# Ajouter une entrée pour le pilote ODBC HFSQL dans odbcinst.ini
RUN echo "[HFSQL] \
Description = HFSQL \
Driver = /codes/ODBC_Linux/wd280hfo64.so" >> /etc/odbcinst.ini

RUN python3 manage.py collectstatic --no-input
#RUN celery -A ProjetDjango1 worker --beat -l info

EXPOSE 8000