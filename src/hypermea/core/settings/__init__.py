import os
from types import ModuleType
from typing import Dict
from hypermea.core.domain import load_domain

import platform
from pydantic import __version__ as pydantic_version
from cerberus import __version__ as cerberus_version
from eve import __version__ as eve_version
from hypermea.core import VERSION as hypermea_core_version

from .promoter import SettingPromoter


def starting_environment() -> Dict:
    from settings.all_settings import get_settings, devops_settings_dump
    all_settings = get_settings()
    from .. import VERSION as service_version

    rtn = {}
    service_name = all_settings.hypermea.service_name

    rtn['versions'] = {
        service_name: service_version,
        "hypermea.core": hypermea_core_version,
        "pydantic": pydantic_version,
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


def build_static_settings(kwargs):
    if 'settings' in kwargs:
        static_settings = kwargs['settings']
    else:
        d = ModuleType('settings')
        with open('static_settings.py') as f:
            exec(f.read(), d.__dict__)
        static_settings = {k: v for k, v in d.__dict__.items() if k.isupper()}
        static_settings['DOMAIN'] = load_domain()

    return static_settings
