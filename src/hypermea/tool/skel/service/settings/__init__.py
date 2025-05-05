import os
from .loader import load_settings_from_env_files

from .hypermea import HypermeaSettings
from .logging import LoggingSettings
from .timezone import TimezoneSettings
from .rate_limit import RateLimitSettings

from integration.mongo.settings import MongoSettings
from integration.smtp.settings import SmtpSettings


if not os.getenv('HYPERMEA_DISABLE_SETTINGS_AUTOLOAD'):
    load_settings_from_env_files([
        HypermeaSettings, LoggingSettings, TimezoneSettings, RateLimitSettings,
        MongoSettings, SmtpSettings
    ])

# Internal registry
_registry = {
    'hypermea': HypermeaSettings(),
    'logging': LoggingSettings(),
    'timezone': TimezoneSettings(),
    'rate_limit': RateLimitSettings(),
    'mongo': MongoSettings(),
    'smtp': SmtpSettings(),
}

# Accessors (used throughout the app)
def get_hypermea(): return _registry['hypermea']
def get_logging(): return _registry['logging']
def get_timezone(): return _registry['timezone']
def get_rate_limit(): return _registry['rate_limit']
def get_mongo(): return _registry['mongo']
def get_smtp(): return _registry['smtp']

# Optionally keep these for default usage
hypermea = get_hypermea()
logging = get_logging()
timezone = get_timezone()
rate_limit = get_rate_limit()
mongo = get_mongo()
smtp = get_smtp()

__all__ = [
    'get_hypermea', 'get_logging', 'get_timezone', 'get_rate_limit', 'get_mongo', 'get_smtp',
    'hypermea', 'logging', 'timezone', 'rate_limit', 'mongo', 'smtp'
]
