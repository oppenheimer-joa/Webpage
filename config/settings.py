# add modules - p192
from pathlib import Path
from configparser import ConfigParser

# set user model - must be on top, p192
AUTH_USER_MODEL = "users.User"

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'ejdqv%f@s4i0qj@l%3o5%(qjw*ju$yz9v7(h+5t-e@xvy*zcsb'

DEBUG = True

ALLOWED_HOSTS = ['192.168.70.89', '34.64.160.47', 'localhost', 'google.com']

INSTALLED_APPS = [
    # add bootstrap4
    'bootstrap4',
    # add post - must be on top, p201
    'posts',
    # add user - must be on top, p191
    'users',
    # add corsheaders'
    'corsheaders',
    'userpage',
    'storages',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]

MIDDLEWARE = [
    # add corsheaders
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# add templates dir - p186
# TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES_DIR = f'{BASE_DIR}/templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # add dirs - p186
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'config.wsgi.application'

config = ConfigParser()
# config.read('config.ini')
config.read('./config/config.ini')

s3_access = config.get("AWS", "S3_ACCESS")
s3_secret = config.get("AWS", "S3_SECRET")

db_host = config.get("MYSQL", "MYSQL_HOST")
db_passwd = config.get("MYSQL", "MYSQL_PWD")
db_port = config.get("MYSQL", "MYSQL_PORT")
db_user = config.get("MYSQL", "MYSQL_USER")
db_name = config.get("MYSQL", "MYSQL_DB")

# AWS RDS
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': f'{db_name}',
        'USER': f'{db_user}',
        'PASSWORD': f'{db_passwd}',
        'HOST': f'{db_host}',
        'PORT': f'{db_port}',  # MySQL 기본 포트
    }
}

AWS_REGION = "ap-northeast-2"
AWS_STORAGE_BUCKET_NAME = "sms-warehouse"
AWS_ACCESS_KEY_ID = s3_access
AWS_SECRET_ACCESS_KEY = s3_secret
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com"

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

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

# change language code
LANGUAGE_CODE = 'ko-kr'

# change timezone
TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# add static dir - p187
STATIC_URL = '/static/'
# STATICFILES_DIR = [BASE_DIR / 'static']
STATICFILES_DIRS = [f'{BASE_DIR}/static']

# add media dir - p187
MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_ROOT = f'{BASE_DIR}/media'

# cors
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

# 문제 일으킬 시 삭제..
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
