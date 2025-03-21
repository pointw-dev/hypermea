"""
Settings to configure Eve's behaviours.
"""
import domain
from configuration import SETTINGS

def eve_passthrough(eve_setting):
    if f'HY_{eve_setting}' in SETTINGS:
        value = SETTINGS[f'HY_{eve_setting}']
        if eve_setting.startswith('RATE_LIMIT_'):
            value = eval(value)
        globals()[eve_setting] = value


if SETTINGS.has_enabled('HY_MONGO_ATLAS'):
    MONGO_URI = f'mongodb+srv://{SETTINGS.get("HY_MONGO_USERNAME")}:{SETTINGS.get("HY_MONGO_PASSWORD")}@{SETTINGS["HY_MONGO_HOST"]}/{SETTINGS["HY_MONGO_DBNAME"]}?retryWrites=true&w=majority'
else:
    MONGO_HOST = SETTINGS.get('HY_MONGO_HOST')
    MONGO_PORT = SETTINGS.get('HY_MONGO_PORT')
    MONGO_DBNAME = SETTINGS.get('HY_MONGO_DBNAME')
    eve_passthrough('MONGO_AUTH_SOURCE')
    eve_passthrough('MONGO_USERNAME')
    eve_passthrough('MONGO_PASSWORD')

eve_passthrough('URL_PREFIX')
eve_passthrough('CACHE_CONTROL')
eve_passthrough('CACHE_EXPIRES')

if 'HY_RATE_LIMIT' in SETTINGS:
    rate = eval(SETTINGS['HY_RATE_LIMIT'])
    RATE_LIMIT_GET = rate
    RATE_LIMIT_POST = rate
    RATE_LIMIT_PATCH = rate
    RATE_LIMIT_DELETE = rate

eve_passthrough('RATE_LIMIT_GET')
eve_passthrough('RATE_LIMIT_POST')
eve_passthrough('RATE_LIMIT_PATCH')
eve_passthrough('RATE_LIMIT_DELETE')

# the default BLACKLIST is ['$where', '$regex'] - the following line turns on regex
MONGO_QUERY_BLACKLIST = ['$where']

RENDERERS = ['hypermea.core.render.HALRenderer']

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
eve_passthrough('PAGINATION_LIMIT')
eve_passthrough('PAGINATION_DEFAULT')
OPTIMIZE_PAGINATION_FOR_SPEED = False


# http://python-eve.org/features.html#operations-log
# OPLOG = True
# OPLOG_ENDPOINT = '_oplog'

SCHEMA_ENDPOINT = '_schema'
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE', 'PUT']

X_DOMAINS = '*'
X_EXPOSE_HEADERS = ['Origin', 'X-Requested-With', 'Content-Type', 'Accept']
X_HEADERS = [
    'Accept',
    'Authorization',
    'If-Match',
    'Access-Control-Expose-Headers',
    'Access-Control-Allow-Origin',
    'Content-Type',
    'Pragma',
    'X-Requested-With',
    'Cache-Control'
]

RETURN_MEDIA_AS_BASE64_STRING = False
RETURN_MEDIA_AS_URL = True

eve_passthrough('MEDIA_BASE_URL')
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']

AUTH_FIELD = '_owner'

DOMAIN = domain.DOMAIN
