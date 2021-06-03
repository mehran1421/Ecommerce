from .base import *

try:
    from config.settings.local import *
except Exception:
    pass

DEBUG = True
ALLOWED_HOSTS = []

DEV_APP = [
    'silk',
]
INSTALLED_APPS += DEV_APP

DEV_MID = [
    'silk.middleware.SilkyMiddleware',
]

MIDDLEWARE += DEV_MID
