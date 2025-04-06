import logging
from hypermea.core.utils import get_operating_environment
from configuration import SETTINGS


def log_operating_environment():
    logger = logging.getLogger("environment")
    logger.info("== dump operating environment ==")
    logger.info("== stack versions")

    operating_environment = get_operating_environment()

    max_key_length = max(len(k) for k in operating_environment['versions'].keys())

    for name, version in operating_environment['versions'].items():
        padding = " " * (max_key_length - len(name) + 1)
        logger.info(f"{name}{padding}{version}")

    logger = logging.getLogger("service")
    SETTINGS.dump(callback=logger.info)

    logger.info("=========== end dump ===========")
