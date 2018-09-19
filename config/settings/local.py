# -*- coding: utf-8 -*-
"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

import socket
import os
from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('DJANGO_SECRET_KEY', default='>/Inf@>Z=rDlKBn;Wfe<Y4i<8;!Wj?w]bMoR0|A=Ni#B<!Klp1')


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_PASSWORD = 'alakwa336278'
# EMAIL_HOST_USER = 'boscoalakwa'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True


DEFAULT_FROM_EMAIL = 'Bitnob'

# this is to ensure the activation email urls follow the convention of the client app

URL_FRONT = 'http://localhost:8080/app/#/'
ACCOUNT_PASSWORD_RESET_CONFIRM = URL_FRONT + 'access/password-reset/confirm/'


#
# EMAIL_BACKEND = "sgbackend.SendGridBackend"
# SENDGRID_API_KEY = "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"

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]
INSTALLED_APPS += ['debug_toolbar', ]

INTERNAL_IPS = ['127.0.0.1', '10.0.2.2', '*']
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['django_extensions', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
CELERY_ALWAYS_EAGER = True
########## END CELERY

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


BVN_API_ENDPOINT = 'https://ravesandboxapi.flutterwave.com/v2/kyc/bvn'

INCLUSIVE_FT_API = 'https://api.inclusiveft.com/v1/GH/search/'
