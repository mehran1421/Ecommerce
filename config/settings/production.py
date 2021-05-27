from .base import *

try:
    from config.settings.local import *
except Exception:
    pass

DEBUG = False
ALLOWED_HOSTS = ['ip-address', 'www.example.com']


