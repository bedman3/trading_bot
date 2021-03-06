"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from main.util.logger.init_logger import get_logger

logger = get_logger(__name__)

import os

from main.util.get_env.django_settings_env import get_debug_from_env

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# from main.service.background import SECRETS_MODEL
# SECRETS_MODEL = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n97(^2#5#r^()72oanwqmml8$pg+pg=do06&loyabn8$1pz7ag'

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = None

DEBUG = get_debug_from_env()

if DEBUG:
    logger.info('Service in debug mode')
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost'
    ]
else:
    logger.info('Service not in debug mode')
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        '*',
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'background_task'
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

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'main/templates')],
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

WSGI_APPLICATION = 'main.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

from main.service.background import SECRETS_MODEL

print(SECRETS_MODEL.DJANGO_DB_PORT)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': SECRETS_MODEL.DJANGO_DB_NAME,
        'USER': SECRETS_MODEL.DJANGO_DB_USERNAME,
        'PASSWORD': SECRETS_MODEL.DJANGO_DB_PASSWORD,
        'HOST': SECRETS_MODEL.DJANGO_DB_HOST,
        'PORT': SECRETS_MODEL.DJANGO_DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": True,
    "LOGIN_URL": "/accounts/login",
    "LOGOUT_URL": "/accounts/logout"
}

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, "main/static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "main/static"),
]
