from .base import *
from decouple import config

DEBUG = True
ALLOWED_HOSTS = []

THIRD_PARTY_APPS = [
    'products_app.apps.ProductsAppConfig',
    'account.apps.AccountConfig',
    'carts.apps.CartsConfig',
    'payment.apps.PaymentConfig',
]

LOCAL_APPS = [
    'rest_framework',
    'django_filters',
]

INSTALLED_APPS += THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE += [
    # my middleware
]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ]
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHE_TTL = 60 * 1

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
