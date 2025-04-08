import socket
from email.policy import default

from hypermea.core.settings import SettingsManager

SETTINGS = SettingsManager.instance()
SETTINGS.set_prefix_description('HY', 'HypermeaService base configuration')
SETTINGS.create('HY', {
    'API_NAME': 'dev-hypermea-api',
    'API_PORT': 2112,
    'INSTANCE_NAME': socket.gethostname(),

    'MONGO_ATLAS': 'Disabled',
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': 27017,
    'MONGO_DBNAME': 'dev-hypermea-api',

    'TRACE_LOGGING': 'Enabled',
    'PAGINATION_LIMIT': 3000,
    'PAGINATION_DEFAULT': 1000,
    'ADD_ECHO': 'Disabled',
    'LOG_TO_FOLDER': 'Disabled',
    'LOG_TO_EMAIL': 'Disabled',
    'LOG_MAX_BODY_SIZE': 1024,
})

# optional settings...
SETTINGS.create('HY', 'USE_ABSOLUTE_URLS', is_optional=True)
SETTINGS.create('HY', 'BASE_PATH', is_optional=True)
SETTINGS.create('HY', 'BASE_URL', is_optional=True)
SETTINGS.create('HY', 'GATEWAY_URL', is_optional=True)
SETTINGS.create('HY', 'NAME_ON_GATEWAY', is_optional=True)
SETTINGS.create('HY', 'URL_PREFIX', is_optional=True)

SETTINGS.create('HY', 'DISABLE_RFC6861', is_optional=True)

SETTINGS.create('HY', 'CACHE_CONTROL', is_optional=True)
SETTINGS.create('HY', 'CACHE_EXPIRES', is_optional=True, default_value=0)

SETTINGS.create('HY', 'FOLDER_TO_LOG_TO', is_optional=True)

SETTINGS.create('HY', 'MONGO_USERNAME', is_optional=True)
SETTINGS.create('HY', 'MONGO_PASSWORD', is_optional=True)
SETTINGS.create('HY', 'MONGO_AUTH_SOURCE', is_optional=True)

SETTINGS.create('HY', 'MEDIA_BASE_URL', is_optional=True)

SETTINGS.create('HY', 'RATE_LIMIT', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_GET', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_POST', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_PATCH', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_DELETE', is_optional=True)


SETTINGS.create('HY', 'LOG_EMAIL_VERBOSITY', is_optional=True, default_value='ERROR')
# SETTINGS.create('HY', 'LOG_EMAIL_PATTERN', default='*')
SETTINGS.create('HY', 'LOG_EMAIL_RECIPIENTS', is_optional=True)
SETTINGS.create('HY', 'LOG_EMAIL_FROM', is_optional=True, default_value=f'{SETTINGS.get("HY_API_NAME")} <no-reply@example.com>')

# cancellable settings...
# if SETTINGS.get('HY_CANCELLABLE') == '':
#     del SETTINGS['HY_CANCELLABLE'] / SETTINGS['HY_CANCELLABLE'].pop()
