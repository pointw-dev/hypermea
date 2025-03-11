import socket
from hypermea.core.settings_manager import SettingsManager

SETTINGS = SettingsManager.instance()
SETTINGS.set_prefix_description('HY', 'HypermeaService base configuration')
SETTINGS.create('HY', {
    'API_NAME': '{$project_name}',
    'API_PORT': 2112,
    'INSTANCE_NAME': socket.gethostname(),

    'MONGO_ATLAS': 'Disabled',
    'MONGO_HOST': 'localhost',
    'MONGO_PORT': 27017,
    'MONGO_DBNAME': '{$project_name}',

    'TRACE_LOGGING': 'Enabled',
    'PAGINATION_LIMIT': 3000,
    'PAGINATION_DEFAULT': 1000,
    'ADD_ECHO': 'Disabled',
    'LOG_TO_FOLDER': 'Disabled',
    'SEND_ERROR_EMAILS': 'Disabled',
    'LOG_MAX_BODY_SIZE': 1024,
})

# optional settings...
SETTINGS.create('HY', 'DISABLE_RFC6861', is_optional=True)
SETTINGS.create('HY', 'USE_ABSOLUTE_URLS', is_optional=True)
SETTINGS.create('HY', 'BASE_PATH', is_optional=True)
SETTINGS.create('HY', 'BASE_URL', is_optional=True)
SETTINGS.create('HY', 'GATEWAY_URL', is_optional=True)
SETTINGS.create('HY', 'NAME_ON_GATEWAY', is_optional=True)
SETTINGS.create('HY', 'URL_PREFIX', is_optional=True)
SETTINGS.create('HY', 'CACHE_CONTROL', is_optional=True)
SETTINGS.create('HY', 'CACHE_EXPIRES', is_optional=True, default_value=0)
SETTINGS.create('HY', 'MONGO_USERNAME', is_optional=True)
SETTINGS.create('HY', 'MONGO_PASSWORD', is_optional=True)
SETTINGS.create('HY', 'MONGO_AUTH_SOURCE', is_optional=True)
SETTINGS.create('HY', 'MEDIA_BASE_URL', is_optional=True)
SETTINGS.create('HY', 'PUBLIC_RESOURCES', is_optional=True)

SETTINGS.create('HY', 'RATE_LIMIT', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_GET', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_POST', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_PATCH', is_optional=True)
SETTINGS.create('HY', 'RATE_LIMIT_DELETE', is_optional=True)


if SETTINGS.has_enabled('HY_SEND_ERROR_EMAILS'):
    SETTINGS.create('HY', 'SMTP_PORT', default_value=25)
    SETTINGS.create('HY', 'SMTP_HOST', is_optional=True)
    SETTINGS.create('HY', 'ERROR_EMAIL_RECIPIENTS', is_optional=True)
    SETTINGS.create('HY', 'ERROR_EMAIL_FROM', is_optional=True)

# cancellable settings...
# if SETTINGS.get('HY_CANCELLABLE') == '':
#     del SETTINGS['HY_CANCELLABLE']
