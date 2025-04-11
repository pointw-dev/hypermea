"""
hooks.logging
This module defines functions to log requests, and to manage log verbosity.
"""
import logging
import json
from flask import make_response, jsonify, request as flask_request
from hypermea.core.logging import trace
from hypermea.core.logging.hooks import log_request, log_response
from hypermea.core.href import get_self_href_from_request
from hypermea.core.response import make_error_response
import settings

LOG = logging.getLogger('hooks.logging')


@trace
def add_hooks(app):
    """Wire up the events for logging"""
    app.on_pre_GET += _log_request
    app.on_pre_POST += _log_post_request
    app.on_pre_PATCH += _log_request
    app.on_pre_PUT += _log_request
    app.on_pre_DELETE += _log_request

    app.on_post_GET += _log_response
    app.on_post_POST += _log_response
    app.on_post_PATCH += _log_response
    app.on_post_PUT += _log_response
    app.on_post_DELETE += _log_response

    @app.route('/_logging', methods=['GET'])
    def get_logging_config():
        """Returns the current verbosity levels for logging handlers."""
        if app.auth and not app.auth.authorized(None, '_logging', 'GET'):
            return make_error_response('Please provide proper credentials', 401)

        return _get_logging_config()

    @app.route('/_logging/edit-form', methods=['GET'])
    def get_logging_edit_form():
        """Returns the current verbosity levels for logging handlers."""
        if app.auth and not app.auth.authorized(None, '_logging', 'GET'):
            return make_error_response('Please provide proper credentials', 401)

        return _get_logging_edit_form()

    @app.route('/_logging', methods=['PUT'])
    def put_logging_config():
        """PUT logging level to handlers."""
        if app.auth and not app.auth.authorized(None, '_logging', 'PUT'):
            return make_error_response('Please provide proper credentials', 401)

        return _put_logging_config()


@trace
def _log_post_request(resource, request):
    log_request(LOG, resource, request, None)

@trace
def _log_request(resource, request, lookup):
    log_request(LOG, resource, request, lookup)

@trace
def _log_response(resource, request, payload):
    log_response(LOG, resource, request, payload)


@trace
def _get_logging_config():
    """Returns the verbosity for all handlers."""
    logger = logging.getLogger()
    payload = {
        handler.name: logging.getLevelName(handler.level)
        for handler in logger.handlers
    }
    payload['_links'] = {
        'self': { 'href': get_self_href_from_request() },
        'edit-form': { 'href': get_self_href_from_request()+'/edit-form' }
    }

    response = make_response(jsonify(payload), 200)
    _log_request('_logging', flask_request, response)
    return response


@trace
def _get_logging_edit_form():
    logger = logging.getLogger()

    properties = []
    for handler in logger.handlers:
        properties.append({
            'name': handler.name,
            'prompt': f'Verbosity level for {handler.name}',
            'required': False,
            'value': logging.getLevelName(handler.level),
            'type': 'string',
            'options': {
                'inline': [
                    'TRACE',
                    'DEBUG',
                    'INFO',
                    'WARNING',
                    'ERROR',
                    'CRITICAL'
                ],
                'maxItems': 1
            }
        })

    rtn = {
        '_links': {'self': {'href': get_self_href_from_request()}},
        '_templates': {
            'default': {
                'method': 'PUT',
                'contentType': 'application/json',
                'properties': properties
            }
        }
    }

    response = make_response(jsonify(rtn), 200)
    _log_request('_logging', flask_request, response)
    return response


@trace
def _put_logging_config():
    """PUTs the verbosity for handlers."""
    response = make_error_response('Could not change log settings', 400)

    try:
        if flask_request.content_type != 'application/json':
            raise TypeError('The request body must be application/json')

        payload = json.loads(flask_request.data)

        logger = logging.getLogger()
        # first loop through to ensure everything is valid
        for key in payload:
            handler = [x for x in logger.handlers if x.name == key]
            if not handler:
                raise ValueError(f'{key} is not a valid log handler')
            try:
                getattr(logging, payload[key])
            except AttributeError:
                raise ValueError(f'{payload[key]} is not a valid log verbosity level')

        # now it's safe to iterate and change levels
        for key in payload:
            handler = [x for x in logger.handlers if x.name == key][0]
            handler.setLevel(getattr(logging, payload[key]))

        payload = {}
        for handler in logger.handlers:
            payload[handler.name] = logging.getLevelName(handler.level)

        response = make_response(jsonify(payload), 200)

    except (TypeError, ValueError) as ex:
        response = make_error_response('Invalid log setting specification', 422, exception=ex)

    except Exception as ex:
        response = make_error_response('Could not change log settings', 400, exception=ex)

    _log_request('_logging', flask_request, response)
    return response
