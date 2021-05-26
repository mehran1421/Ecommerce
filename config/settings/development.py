from .base import *


try:
    from config.settings.local import *
except Exception:
    pass


DEBUG = True
ALLOWED_HOSTS = []

DEV_APP = [

]
INSTALLED_APPS += DEV_APP
