import logging
import json
import socket
from datetime import datetime
from copy import deepcopy
import hashlib
from typing import List, Dict, Optional
import re
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from flask import jsonify, make_response, current_app, request, Response, g, after_this_request
from flask.testing import FlaskClient
from pymongo.database import Database
from eve.utils import document_etag
from datetime import datetime
from bson import ObjectId
from configuration import SETTINGS

LOG = logging.getLogger('utils')

unauthorized_message = {
    "_status": "ERR",
    "_error": {
        "message": "Please provide proper credentials",
        "code": 401
    }
}

not_found_message = {
    "_status": "ERR",
    "_error": {
        "message": "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
        "code": 404
    }
}


def get_db() -> Database:
    return current_app.data.driver.db


def get_api() -> FlaskClient:
    return current_app.test_client()


def make_error_response(message: str, code: int, issues: Optional[List[Dict]] = None, **kwargs):
    if issues is None:
        issues = []

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

    
def url_join(*parts: str) -> str:
    url = ""
    for p in parts:
        p = p.strip()
        if p.startswith('?'):
            # Directly concatenate if part starts with '?'
            url += p
        else:
            # Add a '/' before the part if it's not the first part and the url doesn't already end with '/'
            if url and not url.endswith('/'):
                url += '/'
            url += p.strip('/')

    if url.endswith('/'):
        url = url[:-1]

    return url


def is_mongo_running() -> bool:
    host = SETTINGS['HY_MONGO_HOST']
    port = SETTINGS['HY_MONGO_PORT']
    # TODO: ensure this works with atlas, or other permutations
    try:
        with socket.create_connection((host, port), timeout=0.5):  # TODO: configurable???
            return True
    except OSError:
        return False


def get_my_base_url() -> str:
    if not SETTINGS.get('HY_GATEWAY_URL') and not SETTINGS.has_enabled('HY_USE_ABSOLUTE_URLS'):
        return ''

    if SETTINGS.get('HY_BASE_URL'):
        return SETTINGS.get('HY_BASE_URL')

    base_url = re.sub(r'(.*://)?([^/?]+).*', r'\g<1>\g<2>', request.base_url)
    base_url = url_join(base_url, SETTINGS.get('HY_BASE_PATH', ''))

    if base_url[-1] == '/':
        base_url = base_url[0:-1]

    return base_url


def get_id_field(collection_name: str) -> str:
    return current_app.config['DOMAIN'][collection_name]['id_field']


def get_resource_id(resource: dict, collection_name: str) -> str:
    id_field = get_id_field(collection_name)
    rtn = resource.get(id_field, None)
    if not rtn:
        record = get_db()[collection_name].find_one({"_id": ObjectId(resource['_id'])})
        rtn = record[id_field]
    return rtn


def echo_message() -> Response:
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


def inject_path(base, path, remove_query_string=False):
    parts = base.split('?', 1)
    base_part = parts[0]
    query_string = '?' + parts[1] if len(parts) > 1 else ''

    if remove_query_string:
        query_string = ''

    return url_join(base_part, path, query_string)


def clean_href(href:str) -> str:
    parsed = urlparse(href)
    query_params = parse_qsl(parsed.query, keep_blank_values=True)
    filtered_params = [(k, v) for k, v in query_params if k not in ('links-only', 'pretty')]
    cleaned_query = urlencode(filtered_params, doseq=True)
    cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                              parsed.params, cleaned_query, parsed.fragment))
    return cleaned_url


def add_search_link(self_href: str) -> None:
    where = current_app.config['QUERY_WHERE']
    sort = current_app.config['QUERY_SORT']
    max_results = current_app.config['QUERY_MAX_RESULTS']
    page = current_app.config['QUERY_PAGE']

    return {
        'href': f'{self_href}{{?{where},{sort},{max_results},{page},embed}}',
        'templated': True
    }


def add_etag_header_to_post(_, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_etag' in j:
            g.etag_to_inject = j['_etag']

            @after_this_request
            def inject_etag_header(response):
                response.headers['ETag'] = g.etag_to_inject
                return response
        payload.data = json.dumps(j)


def adjust_etag_and_updated_date(record: dict) -> dict:
    if not ('_etag' in record and '_updated' in record):
        return record

    record['_etag'] = document_etag(record)
    record['_updated'] = datetime.now()

    return record


