import logging
from flask import request, g, make_response, jsonify
from hypermea.core.utils import is_mongo_running, get_db
from hypermea.core.response import make_error_response
from hypermea.core.href import get_my_base_url
from hypermea.core.logging import trace

import hooks._gateway
import hooks._error_handlers
import hooks._settings
import hooks._logs

import affordances
from configuration import SETTINGS


LOG = logging.getLogger('hypermea')

@trace
def add_hypermea_hooks(app):
    app.on_delete_item += _delete_item
    app.on_delete_resource += _delete_resource

    @app.before_request
    def before_request():
        if not is_mongo_running():
            LOG.critical('MongoDB is not accessible with current settings.')
            return make_error_response('MongoDB is not running or is not properly configured', 503)

    @app.after_request
    def rewrite_delete_response(response):
        if request.method == 'DELETE' and response.status_code == 204:
            delete_count = 0
            if hasattr(g, 'delete_count'):
                delete_count = g.delete_count
            self_href = get_my_base_url() + request.full_path
            if self_href.endswith('?'):
                self_href = self_href[:-1]
            body = {
                '_status': 'deleted',
                'delete_count': delete_count,
                '_links': {
                    'self': { 'href': self_href },
                    'home': { 'href': get_my_base_url() + '/'}
                }
            }

            if hasattr(g, 'delete_parent'):
                body['_links']['parent'] = {'href': g.delete_parent}

            return make_response(jsonify(body), 200)
        return response


    if SETTINGS.has_enabled('HY_ADD_ECHO'):
        @app.route('/_echo', methods=['PUT'])
        def _echo_message():
            return echo_message()

def _delete_item(resource, item):
    g.delete_count = 1
    g.delete_parent = resource

def _delete_resource(resource):
    collection = get_db()[resource]
    count = collection.count_documents({})
    g.delete_count = count


def echo_message():
    log = logging.getLogger('echo')
    message = 'PUT {"message": {}/"", "status_code": int}, content-type: "application/json"'
    status_code = 400
    if request.is_json:
        try:
            status_code = int(request.json.get('status_code', status_code))
            message = request.json.get('message', message)
        except ValueError:
            pass

    if status_code < 400:
        log.info(message)
    elif status_code < 500:
        log.warning(message)
    else:
        log.error(message)

    return make_response(jsonify(message), status_code)
