"""
hooks.settings
This module defines functions used by the other hooks modules, and some hooks of its own.
"""
import logging
import platform
from flask import current_app, abort
from hypermea.core.utils import make_error_response
from configuration import SETTINGS, VERSION
from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core.logging import trace


LOG = logging.getLogger('hooks.settings')


@trace
def add_hooks(app):
    """Wire up the events for _settings endpoint."""
    app.on_fetched_resource__settings += _fetch_settings


@trace
def _fetch_settings(response):
    if current_app.auth and not current_app.auth.authorized(None, '_settings', 'GET'):
        abort(make_error_response('Please provide proper credentials', 401))

    del response['_items']
    del response['_meta']

    response['versions'] = {}
    response['settings'] = []

    response['versions'][SETTINGS['HY_API_NAME']] = VERSION
    response['versions']['eve'] = eve_version
    response['versions']['cerberus'] = cerberus_version
    response['versions']['python'] = platform.sys.version

    for prefix in SETTINGS.settings:
        section = {
            'description': f'{SETTINGS.prefix_descriptions.get(prefix, "")}',
            'settings': {}
        }
        for setting in SETTINGS.settings[prefix]:
            value = SETTINGS.settings[prefix][setting]
            if ('PASSWORD' in setting) or ('SECRET' in setting) or ('PRIVATE' in setting):
                value = '***'
            section['settings'][f'{prefix}_{setting}'] = value
        response['settings'].append(section)
