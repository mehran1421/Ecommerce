from .base import *

try:
    from config.settings.local import *
except Exception:
    pass

DEBUG = False
ALLOWED_HOSTS = ['8000', 'www.myecommerce1421.com']


