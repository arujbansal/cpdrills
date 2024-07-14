from cpdrills.settings.base import *

DEBUG = False

ALLOWED_HOSTS = []

CSRF_TRUSTED_ORIGINS = []

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES'
        },
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

STATIC_ROOT = "/home/arujbansal/CP-Platform/cpdrills/static"
