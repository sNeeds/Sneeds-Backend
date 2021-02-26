import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "templates")

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',  # for filtering get queries in DRF
    'drf_yasg',  # for filtering get queries in DRF
    'django_rest_passwordreset',
    'polymorphic',  # For django-polymorphic
    'ckeditor',
    'django_extensions',
    'verification',
    'phonenumber_field',
    'rangefilter',

    'abroadin.apps.docs',
    'abroadin.apps.chats',
    'abroadin.apps.customUtils',
    'abroadin.apps.notifications',
    'abroadin.apps.users.userFiles',
    'abroadin.apps.users.customAuth',
    'abroadin.apps.users.consultants',
    'abroadin.apps.users.socialauth',
    'abroadin.apps.store.storeBase',
    'abroadin.apps.store.carts',
    'abroadin.apps.store.orders',
    'abroadin.apps.store.payments',
    'abroadin.apps.store.applyprofilestore',
    'abroadin.apps.estimation.form',
    'abroadin.apps.estimation.estimations',
    'abroadin.apps.estimation.analyze',
    'abroadin.apps.estimation.similarprofiles',
    'abroadin.apps.data.globaldata',
    'abroadin.apps.data.applydata',
    'abroadin.apps.analytics.events',
    'abroadin.apps.applyprofile',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',

    'dbbackup',
    'django_cleanup',  # should go after your apps
    'debug_toolbar',  # should go after staticfiles
]
# Imported key to prevent circular imports.
from .secure import keys

SECRET_KEY = os.environ.get('SECRET_KEY')

ROOT_URLCONF = 'abroadin.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For per-request translation
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'abroadin.settings.middlewares.middlewares.JWTAuthenticationMiddleware',
    'abroadin.settings.middlewares.middlewares.CORSMiddleware',
    'abroadin.settings.middlewares.middlewares.TimezoneMiddleware',
    'abroadin.settings.middlewares.middlewares.UserActionsMiddleWare',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
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

WSGI_APPLICATION = 'abroadin.wsgi.application'

LANGUAGE_CODE = 'en-us'

USE_I18N = True
USE_TZ = True
TIME_ZONE = 'Asia/Tehran'

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "..", "files"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "..", 'static')

MEDIA_URL = '/files/'
MEDIA_ROOT = 'files'

AUTH_USER_MODEL = 'customAuth.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'abroadin.utils.custom.authentication_classes.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter'
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'EXCEPTION_HANDLER': 'abroadin.utils.custom.exception_handler.exception_handler',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST_IP'),
        'PORT': os.environ.get('DB_HOST_PORT'),
    }
}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, '..', 'translations'),
]

from .config.JWTAuthConfig import SIMPLE_JWT

# Loading API keys
from .celery.celery_config import *

# APIs
from .secure import APIs

SKYROOM_API_KEY = APIs.skyroom
SENDINBLUE_API_KEY = APIs.sendinblue
ZARINPAL_MERCHANT = APIs.zarinpal_merchant
PAKAT_API_KEY = APIs.pakat

# Keys
ALL_SKYROOM_USERS_PASSWORD = keys.ALL_SKYROOM_USERS_PASSWORD

# CORS
from corsheaders.defaults import default_headers

# TODO: Make this accurate
CORS_ALLOW_HEADERS = list(default_headers) + [
    'CLIENT-TIMEZONE',
    'CLIENT_TIMEZONE',
    'HTTP-CLIENT-TIMEZONE',
    'HTTP_CLIENT_TIMEZONE',
    'HTTP_CLIENT-TIMEZONE',
    'authorization',
    'AUTHORIZATION',
    'Authorization'
]

# dbbackup -------
from .secure.APIs import dropbox_abroadin_backups_app

DBBACKUP_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'oauth2_access_token': dropbox_abroadin_backups_app,
}
# TODO: Add PGP encryption.
# ---------------------


# ---------------------
# Because of OPTIONS
# https://github.com/encode/django-rest-framework/issues/5616
from rest_framework import permissions
from abroadin.utils.custom.custom_permissions import CustomIsAuthenticated

# permissions.IsAuthenticated = CustomIsAuthenticated
# ---------------------


# ---------------------
# To prevent 413 error
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
# ---------------------


# ---------------------
# from rest_framework.schemas.generators import BaseSchemaGenerator
# SWAGGER_SETTINGS = {
#     "DEFAULT_GENERATOR_CLASS": "rest_framework.schemas.generators.BaseSchemaGenerator",
# }

# Add new DateTimeFormat
from django.conf.global_settings import DATETIME_INPUT_FORMATS

DATETIME_INPUT_FORMATS += ('%Y-%m-%dT%H:%M:%S',)

VERIFICATION = {
    'VERIFICATIONS': [
        {'type': 'email', 'user_model_field': 'is_email_verified'},
    ],
    'CODE_LENGTH': 6,
    'CONTAINS_NUMERIC': True,
    'CONTAINS_UPPER_ALPHABETIC': False,
    'CONTAINS_LOWER_ALPHABETIC': False,
    'LIFE_TIME_SECOND': 0,
    'LIFE_TIME_MINUTE': 3,
    'LIFE_TIME_HOUR': 0,
    'LIFE_TIME_DAY': 0,
    'LIFE_TIME_PENALTY_SECOND': 60,
}

# django-phonenumber-field config
PHONENUMBER_DB_FORMAT = 'E164'
# ---------------------


# Django Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

