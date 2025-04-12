"""
Settings to configure Eve's behaviours.
"""
from hypermea.core.settings import SettingPromoter
import domain
import settings

promote = SettingPromoter(globals())

########################################################################
DOMAIN = domain.DOMAIN


########################################################################
# change Eve default setting values, keeping them as dev-time
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
# promote Eve settings to deploy-time, hypermea base settings (HY_)
promote.all_to_deploy_time([
    'PAGINATION_LIMIT',
    'PAGINATION_DEFAULT'
])

promote.all_to_deploy_time([
    'CACHE_CONTROL',
    'CACHE_EXPIRES'
])

promote.to_deploy_time('URL_PREFIX')
promote.to_deploy_time('MEDIA_BASE_URL')

promote.all_to_deploy_time([
    'MONGO_HOST',
    'MONGO_PORT',
    'MONGO_DBNAME',
    'MONGO_AUTH_SOURCE',
    'MONGO_USERNAME',
    'MONGO_PASSWORD'
])

if settings.mongo.atlas:
    MONGO_URI = f'mongodb+srv://{settings.mongo.username}:{settings.mongo.password}@{settings.mongo.host}/{settings.mongo.dbname}?retryWrites=true&w=majority'

if settings.rate_limit.rate_limit_global:
    rate = settings.rate_limit.rate_limit_global.as_tuple()
    RATE_LIMIT_GET = rate
    RATE_LIMIT_POST = rate
    RATE_LIMIT_PATCH = rate
    RATE_LIMIT_DELETE = rate

promote.all_to_deploy_time(
    ['RATE_LIMIT_GET',
    'RATE_LIMIT_POST',
    'RATE_LIMIT_PATCH',
    'RATE_LIMIT_DELETE'
])

########################################################################
