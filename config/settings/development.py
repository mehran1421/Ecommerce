from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = []

THIRD_PARTY_APPS = [
    'products_app.apps.ProductsAppConfig',
]

LOCAL_APPS = [
    # install packages
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    # my middleware
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST')
    }
}
