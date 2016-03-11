from .base import *

# To boot with these settings, use the command:
# python3 manage.py runserver --settings=cothranlawoffices.settings.local

DEBUG = True

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
'''
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': '/%s/logs/debug.log' % BASE_DIR,
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }
'''

with open(os.path.join(BASE_DIR, 'secrets.json')) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """
    Get the secrete variable or return explicit exception. See
    2 scoops of django p. 55 for more
    """
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'postgres',
        'PASSWORD': get_secret('POSTGRES_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}
'''