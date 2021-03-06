"""
Django settings for forecast project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from os import environ as env

from mongoengine import connect


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.get("SECRET_KEY", "*FgbQ%XHtXtM4lOKg$6cjq2wyD@Lym*$4kuuaZwWn**dxiH&o")
DEBUG = env.get("DEBUG", 1)
ALLOWED_HOSTS = env.get("ALLOWED_HOSTS", ["*"]).split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "metoffice",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'forecast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'forecast.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
username = env.get("MONGO_INITDB_ROOT_USERNAME", "mongodb_username")
password = env.get("MONGO_INITDB_ROOT_PASSWORD", "mongodb_password")
host = env.get("MONGO_HOST", "mongodb")
port = env.get("MONGO_INITDB_PORT", 27017)
db = env.get("MONGO_INITDB_DATABASE", "mongodb_db")
connect(host=f"mongodb://{username}:{password}@{host}:{port}/{db}?authSource=admin", connect=False)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery
CELERY_RESULT_BACKEND = f'redis://{env.get("REDIS_HOST", "redis")}:6379'
CELERY_BROKER_URL = f'redis://{env.get("REDIS_HOST", "redis")}:6379'

# REST
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}