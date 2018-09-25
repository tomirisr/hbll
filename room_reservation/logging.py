"""
This file is to help define how logging will be done in your application. You
could think of this file as a logging settings file. This file should contain
production ready logging configurations.

WARNING: Don't import settings from Django into this file.
"""
import sys
from logging import getLogger as get_logger

default_config = {
    'handlers': ['console', 'mail_admins'],
    'level': 'ERROR',
}

prysm_config = {
    'handlers': ['prysm'],
    'level': 'INFO',
}

django_requests_config = {
    'handlers': ['console', 'mail_admins'],
    'propagate': True,
    'level': 'ERROR',
}

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# LOGGING CONFIGURATION
config = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s',
        },
        'prod': {
            'format': (
                '[%(asctime)s] %(levelname)s | %(name)s:%(lineno)s | '
                '%(message)s'
            ),
            'datefmt': DATE_FORMAT,
        },
        'simple': {
            'format': '%(levelname)s | %(name)s:%(lineno)s | %(message)s',
            'datefmt': DATE_FORMAT,
        },
    },
    'handlers': {
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'prod',
            'stream': sys.stdout,
        },
        'prysm': {
            'level': 'INFO',
            'class': 'prysm_zombies.logging.PrysmLogging',
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': django_requests_config,
        'prysm': prysm_config,
    }
}

prysm_logger = get_logger('prysm')

# provides prysm logger helper: see
# http://pydocs.lib.byu.edu/django-prysm-zombies for information on how to use
from prysm_zombies.logging import Prysm  # noqa # isort:skip
prysm = Prysm(prysm_logger)
