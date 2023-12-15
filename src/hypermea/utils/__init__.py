import logging
import re
from flask import jsonify, make_response
from flask import current_app, request
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from configuration import SETTINGS

LOG = logging.getLogger('utils')

unauthorized_message = {
    "_status": "ERR",
    "_error": {
        "message": "Please provide proper credentials",
        "code": 401
    }
}


def get_my_base_url():
    if not SETTINGS.get('HY_GATEWAY_URL') and not SETTINGS.has_enabled('HY_USE_ABSOLUTE_URLS'):
        return ''

    if SETTINGS.get('HY_BASE_URL'):
        return SETTINGS.get('HY_BASE_URL')

    base_url = re.sub(r'(.*://)?([^/?]+).*', r'\g<1>\g<2>', request.base_url)
    base_url = url_join(base_url, SETTINGS.get('HY_BASE_PATH', ''))

    if base_url[-1] == '/':
        base_url = base_url[0:-1]

    return base_url


def url_join(*parts):
    return '/'.join([p.strip().strip('/') for p in parts])


def get_id_field(collection_name):
    return current_app.config['DOMAIN'][collection_name]['id_field']


def get_resource_id(resource, collection_name):
    id_field = get_id_field(collection_name)
    rtn = resource.get(id_field, None)
    if not rtn:
        record = get_db()[collection_name].find_one({"_id":ObjectId(resource['_id'])})
        rtn = record[id_field]
    return rtn


def is_mongo_running():
    mongoClient = MongoClient(
        "mongodb://usernameMongo:passwordMongo@localhost:27017/?authMechanism=DEFAULT&authSource=database_name",
        serverSelectionTimeoutMS=500)


def get_db():
    return current_app.data.driver.db


def get_api():
    return current_app.test_client()


def make_error_response(message, code, issues=[], **kwargs):
    if 'exception' in kwargs:
        ex = kwargs.get('exception')
        LOG.exception(message, ex)

        if ex:
            issues.append({
                'exception': {
                    'name': type(ex).__name__,
                    'type': ".".join([type(ex).__module__, type(ex).__name__]),
                    'args': ex.args
                }
            })

    resp = {
        '_status': 'ERR',
        '_error': {
            'message': message,
            'code': code
        }
    }

    if issues:
        resp['_issues'] = issues

    return make_response(jsonify(resp), code)


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
