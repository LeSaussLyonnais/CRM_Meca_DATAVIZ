﻿"""
Django settings for ProjetDjango1 project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7bgby^f&a=nqp=(is=ybap38lcn&%)a7xrqxhj@q7qox8*$y7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'corsheaders',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'django_celery_beat',
    'rest_framework', 
    'BlogApp.apps.BlogappConfig' #Definition de notre application BlogApp avec sa configuration particuliere definie dans le fichier apps
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny']}

CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOWED_ORIGINS = [
    # 'http://127.0.0.1:3000',
    # 'http://localhost:3000',
    # 'http://192.168.31.2:3000',
    # "http://localhost:8000",
    # "http://127.0.0.1:8000",
    # "null",
    # 'http://localhost:3000',
    # 'http://localhost:8000',
    # 'https://localhost:3000',
# ]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Access-Control-Allow-Origin',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'ProjetDjango1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "ProjetDjango1/templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProjetDjango1.wsgi.application'
ASGI_APPLICATION = 'ProjetDjango1.asgi.application' 




# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


# Base de donnée par défault de Django


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
'''
# Configurez votre base de données PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db',
        'USER': 'postgres',
        'PASSWORD': 'reden12345',
        #'HOST':  '172.25.0.2', #  Hostname of the database service
        'HOST': 'db',  # Utiliser le nom du service Docker permet à Django de pouvoir toujours se connecter au conteneur db quel que soit son adresse IP interne
        'PORT': '5432',
    }
}
'''

# Pour ne pas avoir de conflit sur la connexion à redis et donc une erreur, il faut s'assurer de bien définir 'redis' en 'hosts' comme
# ci-dessous pour matcher avec l'url du CELERY_BROKER_URL plus bas 
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('192.168.31.4', 6379)] 
        }
    }
}


# Configurer les URLs pour le broker et le backend de Celery avec le mot de passe
#CELERY_BROKER_URL = f'redis://:@redis:6379/0'
#CELERY_RESULT_BACKEND = f'redis://:@redis:6379/0'
#CELERY_TIMEZONE = 'Europe/Paris'
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = 'redis://192.168.31.4:6379/0'
CELERY_RESULT_BACKEND = 'redis://192.168.31.4:6379/0'

# Paramétrage de la périodicité d'éxecution des tâches par Celery
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "ProjetDjango1/static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# IMPORT_EXPORT_USE_TRANSACTIONS = True   # Pas utile finalement
