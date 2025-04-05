import traceback
import sys
import os
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


from eve import __version__ as eve_version
from cerberus import __version__ as cerberus_version
from hypermea.core import VERSION as hypermea_core_version
from configuration import SETTINGS, VERSION as api_version
import logging
import platform

LOG = logging.getLogger('utils')


def dump_operating_environment():
    logger = logging.getLogger("environment")
    logger.info("== dump operating environment ==")
    logger.info("== stack versions")

    api_name = SETTINGS.get("HY_API_NAME", "api")

    components = {
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

    max_key_length = max(len(k) for k in components.keys())

    for name, version in components.items():
        padding = " " * (max_key_length - len(name) + 1)
        logger.info(f"{name}{padding}{version}")

    logger = logging.getLogger("service")
    SETTINGS.dump(callback=logger.info)

    logger.info("=========== end dump ===========")





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

        tb = traceback.TracebackException.from_exception(ex)
        site_packages_stack = []
        app_stack = []
        hypermea_stack = []
        full_stack = []

        report_stack = True
        separate_stack = True

        for frame in tb.stack:
            path = os.path.relpath(frame.filename)

            stack_item = {
                "line_number": frame.lineno,
                "function": frame.name,
                "code": frame.line.strip() if frame.line else None
            }

            if report_stack:
                if '/hypermea/' in path:
                    stack_item['file'] = 'hypermea/' + path.split('/hypermea/')[1]
                    hypermea_stack.insert(0, stack_item)
                elif 'site-packages' in path:
                    stack_item['file'] = '/site-packages/' + path.split('/site-packages/')[1]
                    site_packages_stack.insert(0, stack_item)
                else:
                    stack_item['file'] = path
                    app_stack.insert(0, stack_item)
            else:
                stack_item['file'] = path
                full_stack.insert(0, stack_item)


        if ex:
            issue = {
                'exception': {
                    'name': type(ex).__name__,
                    'type': ".".join([type(ex).__module__, type(ex).__name__]),
                    'args': ex.args,
                }
            }

            if report_stack:
                if separate_stack:
                    issue.update({
                        'app_stack': app_stack,
                        'hypermea_stack': hypermea_stack,
                        'site_packages_stack': site_packages_stack
                    })
                else:
                    issue.update({'stack': full_stack})

            issues.append(issue)

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

def hal_format_error(data):
    rtn = {
        'status': data.get('_status', "unknown"),
        'status_code': data['_error']['code'],
        'message': data['_error']['message'],
        '_links': {
            "self": request.url
        }
    }

    if '_issues' in data:
        rtn['_embedded'] = {
            "issues": data['_issues']
        }

    return rtn


    
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


def get_resource_rel(resource_name: str) -> str:
    rel = current_app.config['DOMAIN'].get(resource_name, {}).get('link_relation', '')
    rel = rel if rel else resource_name
    return rel


def get_resource_id(resource: dict, collection_name: str) -> str:
    id_field = get_id_field(collection_name)
    rtn = resource.get(id_field, None)
    if not rtn:
        record = get_db()[collection_name].find_one({"_id": ObjectId(resource['_id'])})
        rtn = record[id_field]
    return rtn


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
    filtered_params = [(k, v) for k, v in query_params if k not in ('links_only', 'pretty')]
    cleaned_query = urlencode(filtered_params, doseq=True)
    cleaned_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path,
                              parsed.params, cleaned_query, parsed.fragment))
    return cleaned_url


def add_search_link(self_href: str) -> dict[str, bool | str]:
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


