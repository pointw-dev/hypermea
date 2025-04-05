import logging
import platform

from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core import VERSION as hypermea_core_version
from configuration import SETTINGS, VERSION as api_version


def log_operating_environment():
    logger = logging.getLogger("environment")
    logger.info("== dump operating environment ==")
    logger.info("== stack versions")

    api_name = SETTINGS.get("HY_API_NAME", "api")

    components = {
        api_name: api_version,
        "hypermea.core": hypermea_core_version,
        "eve": eve_version,
        "cerberus": cerberus_version,
        "python": platform.sys.version,
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "os_platform": platform.platform(),
    }

    max_key_length = max(len(k) for k in components.keys())

    for name, version in components.items():
        padding = " " * (max_key_length - len(name) + 1)
        logger.info(f"{name}{padding}{version}")

    logger = logging.getLogger("service")
    SETTINGS.dump(callback=logger.info)

    logger.info("=========== end dump ===========")
