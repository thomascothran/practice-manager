from .base import *

DEBUG = True

SECRET_KEY = os.environ['SECRET_KEY']

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
