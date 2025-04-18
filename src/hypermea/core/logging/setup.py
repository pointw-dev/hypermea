"""
Configure standard python logging
"""

import settings
from hooks._custom_logging import additional_log_setup
from hypermea.core.logging.log_setup import LogSetup


def setup_logger():
    LogSetup(settings.hypermea.service_name)
    additional_log_setup()


setup_logger()
