"""
hooks.settings
This module defines functions used by the other hooks modules, and some hooks of its own.
"""
import logging
from flask import current_app, abort
from hypermea.core.response import make_error_response
from hypermea.core.logging import trace
from hypermea.core.utils import get_operating_environment


LOG = logging.getLogger('hooks.settings')


@trace
def add_hooks(app):
    """Wire up the events for _settings endpoint."""
    app.on_fetched_resource__settings += _fetch_settings


@trace
def _fetch_settings(response):
    if current_app.auth and not current_app.auth.authorized(None, '_settings', 'GET'):
        abort(make_error_response('Please provide proper credentials', 401))

    response.pop('_items')
    response.pop('_meta')

    op_env = get_operating_environment()
    response['versions'] = op_env['versions']
    response['settings'] = op_env['settings']
