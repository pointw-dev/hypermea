import traceback
import os
import logging
import json
import socket
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


def clean_href(href: str) -> str:
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


def inject_path(base, path, remove_query_string=False):
    parts = base.split('?', 1)
    base_part = parts[0]
    query_string = '?' + parts[1] if len(parts) > 1 else ''

    if remove_query_string:
        query_string = ''

    return url_join(base_part, path, query_string)



