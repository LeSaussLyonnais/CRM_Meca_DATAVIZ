# Utiliser une image de base Ubuntu
FROM debian:latest

# Mettre à jour les paquets et installer unixodbc
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev odbcinst unzip python3-pip python3-venv
RUN apt-get update && apt-get install -y libiodbc2-dev
RUN apt-get update && apt-get install -y iodbc
#unixodbc unixodbc-dev

# Créer un environnement virtuel
RUN python3 -m venv /venv

# Activer l'environnement virtuel
ENV PATH="/venv/bin:$PATH"

# Copier le pilote HFSQL et les fichiers de configuration ODBC dans le conteneur

COPY ODBC28LINUX64PACK066p.zip /usr/local/lib/ODBC28LINUX64PACK066p.zip
RUN cd /usr/local/lib/ \
    && unzip /usr/local/lib/ODBC28LINUX64PACK066p.zip \
    && chmod 777 -R ./  \
    && bash install.sh
RUN cd /usr/local/lib/ \
    && mkdir /php-8.3.6/
COPY php-8.3.6-Win32-vs16-x64.zip /usr/local/lib/php-8.3.6/php-8.3.6-Win32-vs16-x64.zip
RUN cd /usr/local/lib/php-8.3.6/ \    
    && unzip /usr/local/lib/php-8.3.6/php-8.3.6-Win32-vs16-x64.zip \
    && chmod 777 -R ./
    #&& ./install.sh

COPY odbcinst.ini /etc/
COPY odbc.ini /etc/

ENV ODBCINI=/etc/odbc.ini
ENV ODBCSYSINI=/etc

# Configurer le pilote ODBC
RUN odbcinst -i -d -f /etc/odbcinst.ini
RUN odbcinst -i -s -l -f /etc/odbc.ini

RUN echo "/usr/local/lib" > /etc/ld.so.conf.d/hfsql.conf && ldconfig

# Votre application ici
WORKDIR /app

COPY requirements.txt /app
RUN pip install gunicorn uvicorn[standard]
RUN pip install -r requirements.txt

COPY ProjetDjango1 ProjetDjango1
COPY BlogApp BlogApp
COPY Dockerfile Dockerfile
COPY manage.py manage.py
#COPY data data
COPY gunicorn.app.conf.py gunicorn.app.conf.py
COPY gunicorn.channel.conf.py gunicorn.channel.conf.py

RUN python3 manage.py collectstatic --no-input
#RUN celery -A ProjetDjango1 worker --beat -l info

EXPOSE 8000