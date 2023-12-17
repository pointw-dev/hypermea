"""
hooks.logging
This module defines functions to log requests, and to manage log verbosity.
"""
import logging
import json
from flask import abort, make_response, jsonify, request as flask_request
from hypermea.core.logging import trace
from hypermea.core.utils import make_error_response

LOG = logging.getLogger('hooks.logging')


@trace
def add_hooks(app):
    """Wire up the events for logging"""
    app.on_post_GET += _log_request
    app.on_post_POST += _log_request
    app.on_post_PATCH += _log_request
    app.on_post_PUT += _log_request
    app.on_post_DELETE += _log_request

    @app.route('/_logging', methods=['GET'])
    def get_logging_config():
        """Returns the current verbosity levels for logging handlers."""
        if app.auth and not app.auth.authorized(None, '_logging', 'GET'):
            return make_error_response('Please provide proper credentials', 401)

        return _get_logging_config()

    @app.route('/_logging', methods=['PUT'])
    def put_logging_config():
        """PUT logging level to handlers."""
        if app.auth and not app.auth.authorized(None, '_logging', 'PUT'):
            return make_error_response('Please provide proper credentials', 401)

        return _put_logging_config()


@trace
def _log_request(resource, request, payload):
    """Event hook to log all requests."""
    requested = resource if resource else 'root'
    LOG.info(f'Request for {requested}: {request} [{payload.status_code}]')
    request_headers = f'{request.headers}'.replace('\n','\n  ').rstrip()
    request_data = json.dumps(json.loads(request.data if request.data else "\"\""))
    response_headers = f'{payload.headers}'.replace('\n','\n  ').rstrip()
    response_data = json.dumps(json.loads(payload.data if payload.data else "\"\""))
    LOG.debug(f'\n-request.values:\n  {request.values.to_dict()}\n'
              f'-request.headers:\n  {request_headers}\n'
              f'-request.data:\n  {request_data}\n'
              f'-response.headers:\n  {response_headers}\n'
              f'-payload.data:\n  {response_data}\n')


@trace
def _get_logging_config():
    """Returns the verbosity for all handlers."""
    logger = logging.getLogger()
    payload = {
        handler.name: logging.getLevelName(handler.level)
        for handler in logger.handlers
    }

    response = make_response(jsonify(payload), 200)
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
