"""
This module defines functions to add affordances.rfc6861.edit-form.
"""
import logging
import json
from flask import make_response, current_app
from utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url
from ._common import generate_hal_forms_template

LOG = logging.getLogger("affordances.rfc6861.edit-form")


def add_affordance(app):
    @app.route("/<collection_name>/<resource_id>/edit-form", methods=["GET"])
    def do_get_edit_form_dummy(collection_name, resource_id):
        if app.auth and (not app.auth.authorized(None, "edit-form", "GET")):
            return make_error_response(unauthorized_message, 401)

        return _do_get_edit_form(collection_name, resource_id)


def add_link(resource, collection_name):
    base_url = get_my_base_url()
    resource_id = get_resource_id(resource, collection_name)

    resource['_links']['edit-form'] = {
        'href': f'{base_url}/{collection_name}/{resource_id}/edit-form',
        'title': 'GET to fetch edit-form'
    }


def _do_get_edit_form(collection_name, resource_id):
    schema = current_app.config['DOMAIN'].get(collection_name, {}).get('schema', {})
    base_url = get_my_base_url()
    self_href = f'{base_url}/{collection_name}/{resource_id}'

    template = generate_hal_forms_template('PUT', schema, self_href)  # TODO: PATCH?  one template for each PUT|PATCH?

    # TODO: is pretty
    response = make_response(json.dumps(template, indent=4), 200)
    response.headers['Content-type'] = 'application/prs.hal-forms+json'
    return response
