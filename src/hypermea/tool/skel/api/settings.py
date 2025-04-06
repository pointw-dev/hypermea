"""
Settings to configure Eve's behaviours.
"""
from hypermea.core.utils import set_eve_setting_from_hypermea_base_setting
import domain
from configuration import SETTINGS

########################################################################
DOMAIN = domain.DOMAIN

########################################################################
# change Eve default setting values, keeping them "static"

RENDERERS = ['hypermea.core.render.HALRenderer']
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# the default BLACKLIST is ['$where', '$regex'] - the following line turns on regex
MONGO_QUERY_BLACKLIST = ['$where']

OPTIMIZE_PAGINATION_FOR_SPEED = False
# set to True: faster with large collections, but you lose _meta.count and `last` page links, and `next` page link appears on last page

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
EXTENDED_MEDIA_INFO = ['content_type', 'name', 'length']

AUTH_FIELD = '_owner'


########################################################################
# "elevate" Eve settings to deploy-time hypermea base settings
set_eve_setting_from_hypermea_base_setting('PAGINATION_LIMIT', globals())
set_eve_setting_from_hypermea_base_setting('PAGINATION_DEFAULT', globals())
set_eve_setting_from_hypermea_base_setting('URL_PREFIX', globals())
set_eve_setting_from_hypermea_base_setting('CACHE_CONTROL', globals())
set_eve_setting_from_hypermea_base_setting('CACHE_EXPIRES', globals())
set_eve_setting_from_hypermea_base_setting('MEDIA_BASE_URL', globals())

set_eve_setting_from_hypermea_base_setting('MONGO_HOST', globals())
set_eve_setting_from_hypermea_base_setting('MONGO_PORT', globals())
set_eve_setting_from_hypermea_base_setting('MONGO_DBNAME', globals())
set_eve_setting_from_hypermea_base_setting('MONGO_AUTH_SOURCE', globals())
set_eve_setting_from_hypermea_base_setting('MONGO_USERNAME', globals())
set_eve_setting_from_hypermea_base_setting('MONGO_PASSWORD', globals())

if SETTINGS.has_enabled('HY_MONGO_ATLAS'):
    MONGO_URI = f'mongodb+srv://{SETTINGS.get("HY_MONGO_USERNAME")}:{SETTINGS.get("HY_MONGO_PASSWORD")}@{SETTINGS["HY_MONGO_HOST"]}/{SETTINGS["HY_MONGO_DBNAME"]}?retryWrites=true&w=majority'

if 'HY_RATE_LIMIT' in SETTINGS:
    rate = eval(SETTINGS['HY_RATE_LIMIT'])
    RATE_LIMIT_GET = rate
    RATE_LIMIT_POST = rate
    RATE_LIMIT_PATCH = rate
    RATE_LIMIT_DELETE = rate

set_eve_setting_from_hypermea_base_setting('RATE_LIMIT_GET', globals())
set_eve_setting_from_hypermea_base_setting('RATE_LIMIT_POST', globals())
set_eve_setting_from_hypermea_base_setting('RATE_LIMIT_PATCH', globals())
set_eve_setting_from_hypermea_base_setting('RATE_LIMIT_DELETE', globals())

########################################################################
