"""
This module defines functions to add affordances.rfc6861.create-form.
"""
import logging
import json
from flask import make_response, current_app, request
from hypermea.core.response import make_error_response, unauthorized_message
from hypermea.core.href import get_self_href_from_request, get_my_base_url, inject_path
from ._common import generate_hal_form, get_allowed_methods
import settings

LOG = logging.getLogger("affordances.rfc6861.create-form")


def add_affordance(app):
    @app.route("/<collection_name>/create-form", methods=["GET"])
    def do_get_create_form(collection_name):
        if app.auth and (not app.auth.authorized(None, "edit-form", "GET")):
            return make_error_response(unauthorized_message, 401)

        return _do_get_create_form(collection_name)

    @app.route("/<parent_collection_name>/<parent_id>/<collection_name>/create-form", methods=["GET"])
    def do_get_create_sub_form(parent_collection_name, parent_id, collection_name):
        if app.auth and (not app.auth.authorized(None, "edit-form", "GET")):
            return make_error_response(unauthorized_message, 401)

        return _do_get_create_form(collection_name, (parent_collection_name, parent_id))


def add_link(collection, collection_name, self_href=''):
    if settings.hypermea.disable_rfc6861:
        return
    if 'POST' not in get_allowed_methods(current_app, collection_name)['resource_methods']:
        return

    url = get_self_href_from_request()
    collection['_links']['create-form'] = {
        'href': inject_path(url, 'create-form', True),
        '_note': f'GET to fetch create-form'
    }


def _do_get_create_form(collection_name, parent=None):
    LOG.info(f'GET create-form for {f"{parent[0]}/{parent[1]}/{collection_name}" if parent else f"{collection_name}"}')

    if settings.hypermea.disable_rfc6861:
        return make_error_response('RFC6861 links are disabled.', 404)

    base_url = get_my_base_url()
    schema = current_app.config['DOMAIN'].get(collection_name, {}).get('schema', {})

    parent_segment = ''
    if parent:
        parent_collection_name, parent_id = parent
        parent_segment = f'/{parent_collection_name}/{parent_id}'

    self_href = f'{base_url}{parent_segment}/{collection_name}'

    if 'POST' not in get_allowed_methods(current_app, collection_name)['resource_methods']:
        return make_error_response(f'Cannot add items to the {collection_name} collection, so the corresponding create-form cannot be found.', 404)

    template = generate_hal_form('create', schema, self_href)

    data = json.dumps(template, indent=4 if 'pretty' in request.args else None)
    response = make_response(data, 200)
    response.headers['Content-type'] = 'application/prs.hal-forms+json'
    return response
