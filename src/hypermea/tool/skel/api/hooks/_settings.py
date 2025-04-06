"""
hooks.settings
This module defines functions used by the other hooks modules, and some hooks of its own.
"""
import logging
from flask import current_app, abort, jsonify
from hypermea.core.response import make_error_response
from hypermea.core.logging import trace
from hypermea.core.utils import get_operating_environment


LOG = logging.getLogger('hooks.settings')


@trace
def add_hooks(app):
    """Wire up the route for the _settings endpoint."""
    @app.route('/_settings', methods=['GET'])
    def get_settings():
        """Returns the versions and settings."""
        if app.auth and not app.auth.authorized(None, '_settings', 'GET'):
            return make_error_response('Please provide proper credentials', 401)

        return _get_settings()


@trace
def _get_settings():
    if current_app.auth and not current_app.auth.authorized(None, '_settings', 'GET'):
        abort(make_error_response('Please provide proper credentials', 401))

    return jsonify(get_operating_environment())
