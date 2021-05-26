env_name = 'dev'

if env_name == 'prod':
    from .production import *
elif env_name == 'dev':
    from .development import *