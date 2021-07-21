env_name = 'dev'
is_test_server = True

if env_name == 'prod':
    from .production import *
elif env_name == 'dev':
    from .development import *
