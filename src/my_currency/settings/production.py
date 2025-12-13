import os

from .base import *  # noqa: F403

DEBUG = False

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': os.environ.get('DB_ENGINE'),
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('DB_NAME'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'PORT': os.environ.get('DB_PORT'),
        'USER': os.environ.get('DB_USER'),
    },
}
