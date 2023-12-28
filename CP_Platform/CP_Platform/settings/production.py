from CP_Platform.settings.base import *

DEBUG = False

# All allowed URLs without any prefix. Eg. 'cpdrills.com'
ALLOWED_HOSTS = []

# All allowed URLs with "https://" prefix. Eg. 'https://cpdrills.com'
CSRF_TRUSTED_ORIGINS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
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

STATIC_ROOT = ""
