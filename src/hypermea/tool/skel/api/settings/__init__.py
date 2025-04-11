import os
from .loader import load_ordered_env_files

from .hypermea import HypermeaSettings
from .logging import LoggingSettings
from .rate_limit import RateLimitSettings

from integration.mongo.settings import MongoSettings
from integration.smtp.settings import SmtpSettings


if not os.getenv('HYPERMEA_DISABLE_SETTINGS_AUTOLOAD'):
    load_ordered_env_files([
        HypermeaSettings, LoggingSettings, RateLimitSettings,
        MongoSettings, SmtpSettings
    ])

# Internal registry
_registry = {
    'hypermea': HypermeaSettings(),
    'logging': LoggingSettings(),
    'rate_limit': RateLimitSettings(),
    'mongo': MongoSettings(),
    'smtp': SmtpSettings(),
}

# Accessors (used throughout the app)
def get_hypermea(): return _registry['hypermea']
def get_logging(): return _registry['logging']
def get_rate_limit(): return _registry['rate_limit']
def get_mongo(): return _registry['mongo']
def get_smtp(): return _registry['smtp']

# Optionally keep these for default usage
hypermea = get_hypermea()
logging = get_logging()
rate_limit = get_rate_limit()
mongo = get_mongo()
smtp = get_smtp()

__all__ = [
    'get_hypermea', 'get_logging', 'get_rate_limit', 'get_mongo', 'get_smtp',
    'hypermea', 'logging', 'rate_limit', 'mongo', 'smtp'
]


