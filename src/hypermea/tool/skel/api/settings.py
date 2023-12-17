"""
Settings to configure Eve's behaviours.
"""
import domain
from configuration import SETTINGS


if SETTINGS.has_enabled('HY_MONGO_ATLAS'):
    MONGO_URI = f'mongodb+srv://{SETTINGS.get("HY_MONGO_USERNAME")}:{SETTINGS.get("HY_MONGO_PASSWORD")}@{SETTINGS["HY_MONGO_HOST"]}/{SETTINGS["HY_MONGO_DBNAME"]}?retryWrites=true&w=majority'
else:
    MONGO_HOST = SETTINGS.get('HY_MONGO_HOST')
    MONGO_PORT = SETTINGS.get('HY_MONGO_PORT')
    MONGO_DBNAME = SETTINGS.get('HY_MONGO_DBNAME')
    if 'HY_MONGO_AUTH_SOURCE' in SETTINGS:
        MONGO_AUTH_SOURCE = SETTINGS.get('HY_MONGO_AUTH_SOURCE')
    if 'HY_MONGO_USERNAME' in SETTINGS:
        MONGO_USERNAME = SETTINGS.get('HY_MONGO_USERNAME')
    if 'HY_MONGO_PASSWORD' in SETTINGS:
        MONGO_PASSWORD = SETTINGS.get('HY_MONGO_PASSWORD')

if "HY_URL_PREFIX" in SETTINGS:
    URL_PREFIX = SETTINGS.get("HY_URL_PREFIX")
if "HY_CACHE_CONTROL" in SETTINGS:
    CACHE_CONTROL = SETTINGS.get("HY_CACHE_CONTROL")
if "HY_CACHE_EXPIRES" in SETTINGS:
    CACHE_EXPIRES = SETTINGS.get("HY_CACHE_EXPIRES")

# the default BLACKLIST is ['$where', '$regex'] - the following line turns on regex
MONGO_QUERY_BLACKLIST = ['$where']

RENDERERS = ['hypermea.core.render.HALRenderer']

DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
PAGINATION_LIMIT = SETTINGS.get('HY_PAGINATION_LIMIT')
PAGINATION_DEFAULT = SETTINGS.get('HY_PAGINATION_DEFAULT')
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

if 'HY_MEDIA_BASE_URL' in SETTINGS:
    MEDIA_BASE_URL = SETTINGS.get('HY_MEDIA_BASE_URL')
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']

AUTH_FIELD = '_tenant'
DOMAIN = domain.DOMAIN
