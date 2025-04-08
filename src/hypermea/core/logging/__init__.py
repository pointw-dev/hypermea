import logging
from .trace.trace_level import TRACE_LEVEL
from .trace.decorators import trace
from hypermea.core.settings import starting_environment

from configuration import SETTINGS


@trace
def log_starting_environment():
    logger = logging.getLogger("environment")
    logger.info("== dump starting environment ==")
    logger.info("== stack versions")

    start_env = starting_environment()

    max_key_length = max(len(k) for k in start_env['versions'].keys())

    for name, version in start_env['versions'].items():
        padding = " " * (max_key_length - len(name) + 1)
        logger.info(f"{name}{padding}{version}")

    logger = logging.getLogger("service")
    SETTINGS.dump(callback=logger.info)

    logger.info("=========== end dump ===========")
