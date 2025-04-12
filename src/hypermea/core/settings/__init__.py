import json
import platform
from typing import Dict

from cerberus import __version__ as cerberus_version
from eve import __version__ as eve_version
from hypermea.core import VERSION as hypermea_core_version

from .promoter import SettingPromoter


def starting_environment() -> Dict:
    from settings.all_settings import get_settings, devops_settings_dump
    all_settings = get_settings()
    from .. import VERSION as api_version

    rtn = {}
    api_name = all_settings.hypermea.api_name

    rtn['versions'] = {
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

    rtn['settings_groups'] = devops_settings_dump()

    return rtn
