import logging
from .trace.trace_level import TRACE_LEVEL
from .trace.decorators import trace
from hypermea.core.settings import starting_environment

import settings


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
    settings_groups = start_env['settings_groups']
    for group in settings_groups:
        if not group.get('settings', {}):
            continue
        logger.info(f'== {group["description"]}')
        for setting, value in group['settings'].items():
            logger.info(f'{setting}: {value}')

    logger.info('=========== end dump ===========')
