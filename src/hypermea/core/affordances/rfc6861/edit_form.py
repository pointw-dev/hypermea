"""
This module defines functions to add affordances.rfc6861.edit-form.
"""
import logging
import json
from flask import make_response, current_app, request
from bson.objectid import ObjectId
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url, get_db
from ._common import generate_hal_form, get_allowed_methods
from configuration import SETTINGS

LOG = logging.getLogger("affordances.rfc6861.edit-form")


def add_affordance(app):
    @app.route("/<collection_name>/<resource_id>/edit-form", methods=["GET"])
    def do_get_edit_form_dummy(collection_name, resource_id):
        if app.auth and (not app.auth.authorized(None, "edit-form", "GET")):
            return make_error_response(unauthorized_message, 401)

        return _do_get_edit_form(collection_name, resource_id)


def add_link(resource, collection_name):
    if SETTINGS.has_enabled('HY_DISABLE_RFC6861'):
        return
    allowed_methods = get_allowed_methods(current_app, collection_name)['item_methods']
    if not any(method in allowed_methods for method in ['PATCH', 'PUT']):
        return

    base_url = get_my_base_url()
    resource_id = get_resource_id(resource, collection_name)

    resource['_links']['edit-form'] = {
        'href': f'{base_url}/{collection_name}/{resource_id}/edit-form',
        'title': 'GET to fetch edit-form'
    }


def _do_get_edit_form(collection_name, resource_id):
    LOG.info(f'GET edit-form for {collection_name}:{resource_id}')

    schema = current_app.config['DOMAIN'].get(collection_name, {}).get('schema', {})
    base_url = get_my_base_url()
    self_href = f'{base_url}/{collection_name}/{resource_id}'

    id_field = get_id_field(collection_name)
    search_for = ObjectId(resource_id) if id_field == '_id' else resource_id
    resource = get_db()[collection_name].find_one({id_field: search_for})

    template = generate_hal_form('edit', schema, self_href, resource)

    data = json.dumps(template, indent=4 if 'pretty' in request.args else None)
    response = make_response(data, 200)
    response.headers['Content-type'] = 'application/prs.hal-forms+json'
    return response
