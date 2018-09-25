# -*- coding: utf-8 -*-
"""
Django settings for room_reservation project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/

"""
from os import environ
from pathlib import Path

from django.conf import ImproperlyConfigured

import configuro
import pymysql

from . import logging as logging_config

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------

# setup mysql backend
pymysql.install_as_MySQLdb()

# configuration
BASE_DIR = Path(__file__).parent.parent.absolute()

validation_yaml_file = BASE_DIR / 'config.example.yml'
config_yaml_file = Path(environ.get('DJANGO_CONFIG', BASE_DIR / 'config.yml'))

try:
    config = configuro.YamlConfig.from_validated_yaml_files(
        validation_yaml_file, config_yaml_file
    )
except Exception:
    raise ImproperlyConfigured(
        'Your config.yml file is not configured properly.'
    )

CONFIG = config
PROJECT_NAME = config['meta']['project_slug']
DEBUG = config['general']['debug']
APPS_SITE = config['general']['apps_site']
default_script_name = f'/{PROJECT_NAME}' if APPS_SITE else '/'
FORCE_SCRIPT_NAME = config.safe(
    'general/force_script_name', default=default_script_name
)
SECRET_KEY = config['security']['secret_key']

# APP CONFIGURATION
# ------------------------------------------------------------------------------
# Apps specific for this project go here.
LOCAL_APPS = [
    # Your stuff: custom apps go here
    'core',
    'room_reservation',
    'room',
]

THIRD_PARTY_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    # 'django.contrib.admin',
    'hijack',
    'hijack_admin',
    'compat',
    'rest_framework',
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'core.middleware.PingViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
ADMINS = config['general']['admins']
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
DATABASES = {}

for name, db in config['database'].items():
    DATABASES[name] = {
        'ENGINE': db['engine'],
        'NAME': db['name'],
        'USER': db.get('user', ''),
        'PASSWORD': db.get('password', ''),
        'HOST': db.get('host', ''),
        'PORT': db.get('port', ''),
        'OPTIONS': db.get('options', configuro.Config()).copy_as_dict(),
    }

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
TIME_ZONE = 'America/Denver'
LANGUAGE_CODE = 'en-us'

USE_I18N = False
USE_L10N = True
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # for template dirs not in app_name/templates
        'APP_DIRS': True,  # autodiscovers templates in app_name/templates
        'OPTIONS': {
            'debug': DEBUG,
            'string_if_invalid': '!!missing!!' if DEBUG else '',
            'context_processors': [
                # defaults
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'  # noqa
STATIC_ROOT = config.safe('static/root', default=BASE_DIR / 'static')
STATIC_URL = config.safe('static/url', default=f'{FORCE_SCRIPT_NAME}static/')

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# MEDIA_ROOT = config.safe('media/root', default=BASE_DIR / 'media')
# MEDIA_URL = config.safe('media/url', default=f'{FORCE_SCRIPT_NAME}media/')

# SECURITY and HOST SETTINGS
# ------------------------------------------------------------------------------
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if APPS_SITE:
    PROD_HOST = 'apps.lib.byu.edu'
    STG_HOST = 'appsstg.lib.byu.edu'
    DEV_HOST = f'appsdev.lib.byu.edu'
else:
    PROD_HOST = f'{PROJECT_NAME}.lib.byu.edu'
    STG_HOST = f'{PROJECT_NAME}stg.lib.byu.edu'
    DEV_HOST = f'{PROJECT_NAME}dev.lib.byu.edu'

ALLOWED_HOSTS = config['general'].get(
    'allowed_hosts', [
        PROD_HOST,
        STG_HOST,
        DEV_HOST,
        'localhost',
        '127.0.0.1',
    ]
)

HTTP_X_FORWARDED_HOST = ALLOWED_HOSTS[0]

secure_cookies = config.safe('security/secure_cookies', default=True)

# session settings
SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 hours of inactivity
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = secure_cookies
SESSION_COOKIE_HTTPONLY = True

# security settings
CSRF_COOKIE_SECURE = secure_cookies
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = config.safe('security/ssl_redirect', default=True)
X_FRAME_OPTIONS = 'DENY'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = f'{PROJECT_NAME}.urls'
WSGI_APPLICATION = f'{PROJECT_NAME}.wsgi.application'

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
LOGIN_URL = f'{FORCE_SCRIPT_NAME}login/'
LOGOUT_URL = f'{FORCE_SCRIPT_NAME}logout/'
LOGIN_URL_REGEX = r'^login/$'
LOGOUT_URL_REGEX = r'^logout/$'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend', ]

# CACHE CONFIGURATION
# ------------------------------------------------------------------------------
CACHES = {}
for cache_name, props in config.safe('caches', default={}).items():
    CACHES[cache_name] = {k.upper(): v for k, v in props.items()}

# LOGGING CONFIGURATION
# ------------------------------------------------------------------------------
LOGGING = logging_config.config
# The code below sets up the default_config (for logging) for each of the local
# applications to this project. Just make sure you add local applications into
# the LOCAL_APPS list above.
for app in LOCAL_APPS:
    LOGGING['loggers'][app] = logging_config.default_config

# To log do it the normal way:
# import logging
# logger = logging.getLogger(__name__)
# Or the more pythonic way:
# from config import logging
# logger = logging.get_logger(__name__)

# THIRD-PARTY APP SETTINGS
# ------------------------------------------------------------------------------
# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # for public apis authorization
        'core.permissions.HasAPIGroupPermission',
        # for ajax apis authorizations
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # for public apis auth
        'rest_framework.authentication.BasicAuthentication',
        # for ajax apis auth
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_PAGINATION_CLASS':
    ('rest_framework.pagination.PageNumberPagination'),
    'PAGE_SIZE': 10,
}

# PRYSM SETTINGS
PRYSM_ENABLED = config.safe('prysm/enabled', default=False)

if PRYSM_ENABLED:
    PRYSM_HOST = config['prysm']['host']
    PRYSM_LOG = config['prysm']['log']
    MIDDLEWARE.append('prysm_zombies.middleware.ZombieMiddleware')

# HIJACK SETTINGS
HIJACK_ALLOW_GET_REQUESTS = True
HIJACK_LOGIN_REDIRECT_URL = '/'
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user/'

# CAS SETTINGS
CAS_ENABLED = config.safe('cas/enabled', default=False)

# TESTING and DEBUG modes
if environ.get('RUNNING_TESTS', False):
    FORCE_SCRIPT_NAME = '/'
    STATIC_URL = '/static/'
    # MEDIA_URL = '/media/'
    LOGIN_URL = '/login/'
    LOGOUT_URL = '/logout/'
    SECURE_SSL_REDIRECT = False
    TEMPLATES[0]['OPTIONS']['debug'] = False
    TEMPLATES[0]['OPTIONS']['string_if_invalid'] = ''
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'  # noqa
    CAS_ENABLED = True

elif DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

    # dev specific logging changes
    logging_config.prysm_config['handlers'].append('console')
    logging_config.default_config['handlers'].append('console')
    logging_config.default_config['level'] = 'DEBUG'

    # set default dev server port to the same port as production
    RUNSERVERPLUS_SERVER_ADDRESS_PORT = str(config['general']['port'])

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # shut off some security settings for development
    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SECURE = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'

# CAS
if CAS_ENABLED:
    CAS_SERVER_URL = config.safe(
        'cas/server', default='http://www.jasig.org/cas'
    )
    CAS_LOGOUT_COMPLETELY = True
    CAS_IGNORE_REFERER = True
    CAS_EXTRA_LOGIN_PARAMS = None
    MIDDLEWARE.append('cas.middleware.CASMiddleware')
    INSTALLED_APPS.append('cas')
    AUTHENTICATION_BACKENDS.append('cas.backends.CASBackend')
