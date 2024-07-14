import os
from cpdrills.settings.base import *

DEBUG = True

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

ALLOWED_HOSTS = ['*']

