import logging
import platform
import socket
from flask import current_app
from flask.testing import FlaskClient
from pymongo.database import Database

from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core import VERSION as hypermea_core_version
from configuration import SETTINGS, VERSION as api_version


LOG = logging.getLogger('hypermea')


def get_db() -> Database:
    return current_app.data.driver.db


def get_api() -> FlaskClient:
    return current_app.test_client()


def is_mongo_running() -> bool:
    host = SETTINGS['HY_MONGO_HOST']
    port = SETTINGS['HY_MONGO_PORT']
    # TODO: ensure this works with atlas, or other permutations
    try:
        with socket.create_connection((host, port), timeout=0.5):  # TODO: configurable???
            return True
    except OSError:
        return False


def set_eve_setting_from_hypermea_base_setting(eve_setting, globals):
    if f'HY_{eve_setting}' in SETTINGS:
        value = SETTINGS[f'HY_{eve_setting}']
        if eve_setting.startswith('RATE_LIMIT_'):
            value = eval(value)
        globals[eve_setting] = value


def get_operating_environment():
    rtn = {}
    api_name = SETTINGS.get("HY_API_NAME", "api")

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

    rtn['settings_groups'] = []
    for prefix in SETTINGS.settings:
        group = {
            'description': f'{SETTINGS.prefix_descriptions.get(prefix, "")}',
            'settings': {}
        }
        for setting in SETTINGS.settings[prefix]:
            value = SETTINGS.settings[prefix][setting]
            if ('PASSWORD' in setting) or ('SECRET' in setting) or ('PRIVATE' in setting):
                value = '***'
            group['settings'][f'{prefix}_{setting}'] = value
        rtn['settings_groups'].append(group)

    return rtn
