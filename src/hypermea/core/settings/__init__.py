import platform
from typing import Dict

from cerberus import __version__ as cerberus_version
from eve import __version__ as eve_version
from hypermea.core import VERSION as hypermea_core_version

from .promoter import SettingPromoter


def starting_environment() -> Dict:
    import settings
    from .. import VERSION as api_version

    rtn = {}
    api_name = settings.hypermea.api_name

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
    #
    # rtn['settings_groups'] = []
    # for prefix in SETTINGS.settings:
    #     group = {
    #         'description': f'{SETTINGS.prefix_descriptions.get(prefix, "")}',
    #         'settings': {}
    #     }
    #     for setting in SETTINGS.settings[prefix]:
    #         value = SETTINGS.settings[prefix][setting]
    #         if ('PASSWORD' in setting) or ('SECRET' in setting) or ('PRIVATE' in setting):
    #             value = '***'
    #         group['settings'][f'{prefix}_{setting}'] = value
    #     rtn['settings_groups'].append(group)
    #
    return rtn
