from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = []

THIRD_PARTY_APPS = [
    'products_app.apps.ProductsAppConfig',
    'account.apps.AccountConfig',
]

LOCAL_APPS = [
    'rest_framework',
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    # my middleware
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_NAME'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST')
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# for custom user models
AUTH_USER_MODEL = 'account.User'
