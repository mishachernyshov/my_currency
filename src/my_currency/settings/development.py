import os

from .base import *  # noqa: F403

DEBUG = True

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql'),
        'HOST': os.environ.get('DB_HOST', 'postgres-db'),
        'NAME': os.environ.get('DB_NAME', 'my_currency_db'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'strong_password'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'USER': os.environ.get('DB_USER', 'my_currency_admin'),
    },
}
