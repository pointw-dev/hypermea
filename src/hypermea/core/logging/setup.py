"""
Configure standard python logging
"""


try:
    # this ensures the integration SETTINGS (if they exist) are loaded before the dump
    import integration
except ImportError:
    pass

from configuration import SETTINGS, additional_log_configuration
from hypermea.core.logging.configurator import LogConfigurator


def configure_logger():
    api_name = SETTINGS.get('HY_API_NAME')
    LogConfigurator(api_name)
    additional_log_configuration()


configure_logger()
