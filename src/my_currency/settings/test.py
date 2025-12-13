import os

from .base import *  # noqa: F403

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', 'test_auth_db'),
    },
}
