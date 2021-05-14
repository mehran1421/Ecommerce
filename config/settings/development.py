from .base import *

DEBUG = True
ALLOWED_HOSTS = []

THIRD_PARTY_APPS = [
    # my app
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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
