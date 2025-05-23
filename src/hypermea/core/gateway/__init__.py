import logging
import json
import requests
from requests.exceptions import ConnectionError
from flask import current_app, request
from hypermea.core.logging import trace
import settings

LOG = logging.getLogger('gateway')
REGISTRATIONS = {}


def register(app):
    if not settings.hypermea.gateway_url:
        return

    if not settings.hypermea.base_url:
        LOG.warning('HY_GATEWAY_URL is set, but cannot register because HY_BASE_URL is not set - cancelling')
        return

    url = get_href_from_gateway('gateway_registrations')
    name = settings.hypermea.service_name if not settings.hypermea.name_on_gateway else settings.hypermea.name_on_gateway
    base_url = settings.hypermea.base_url
    LOG.info(f'Registering with gateway as {name} at {base_url} to {url}')
    api = app.test_client()
    response = api.get('/')
    document = response.json
    rels = document.get('_links', {})

    if rels:
        body = {
            'name': name,
            'baseUrl': base_url,
            'rels': rels
        }
        data = json.dumps(body)
        headers = {'content-type': 'application/json'}

        try:
            prior_registration = _get_prior_registration(url, name)
            if prior_registration is None:
                response = requests.post(url, data=data, headers=headers)
            else:
                etag = prior_registration['_etag']
                url = prior_registration['_links']['self']['href']
                headers = {
                    'content-type': 'application/json',
                    'If-Match': etag
                }
                response = requests.put(url, data=data, headers=headers)
            if response.status_code >= 400:
                LOG.error(f'Could not register rels: {response.content}')
        except ConnectionError:
            LOG.warning(f'Could not connect to API gateway at {url} - cancelling')
        # TODO: handle response
    else:
        LOG.warning('No rels to register - cancelling')


def get_href_from_gateway(rel):
    # ASSERT: HY_GATEWAY_URL is set
    # ASSERT: the gateway it points to is up and running
    # ASSERT: the rel is afforded on the gateway
    global REGISTRATIONS
    url = f'{settings.hypermea.gateway_url}/'
    etag = REGISTRATIONS.get('_etag')
    headers = {}
    if etag:
        headers = {
            'If-Not-Match': etag
        }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        REGISTRATIONS = response.json()

    # TODO: handle the very unlikely event that there are two of the same business resource
    # TODO: document how curies work, and how they are used to manage rel collisions - esp. for the non-business rels
    #  e.g. _logging, _settings, etc.
    return REGISTRATIONS.get('_links', {}).get(rel, {}).get('href', '')  # TODO: robustify


def _get_prior_registration(url, name):
    prior_registration = None

    try:
        # response = requests.get(f'{url}/{name}')  # TODO: why did gateway's additional_lookup stop working?
        # if response.status_code == 404:
        #     return None
        # prior_registration = response.json()

        response = requests.get(f'{url}?where={{"name":"{name}"}}')
        prior_registration = response.json()['_items'][0]
    except:
        pass

    return prior_registration


def handle_post_from_external(resource, request):
    if 'where' not in request.args:
        return
    where = json.loads(request.args['where'])  # ASSERT: is json format, etc.
    if not len(where) == 1:
        return
    field = list(where.keys())[0]
    external_id = where[field]
    definition = current_app.config['DOMAIN'][resource]['schema'][field]
    external_relation = definition.get('external_relation', {})
    if not external_relation:
        return

    document = json.loads(request.get_data())  # ASSERT: is json format, etc
    document[field] = external_id
    request._cached_data = json.dumps(document).encode('utf-8')


@trace
def embed_external_parent_resource(resource, request, payload):
    embed_key = 'embedded'
    if embed_key not in request.args:
        return
    embeddable = json.loads(request.args[embed_key])
    for field in embeddable:
        if embeddable[field] and field.find('.') < 0:
            definition = current_app.config['DOMAIN'][resource]['schema'].get(field)
            if not definition:
                return
            external_relation = definition.get('external_relation', {})
            rel = external_relation.get('rel')
            if rel and external_relation.get('embeddable', False):
                response = json.loads(payload.data)
                if field in response:
                    response[field] = _get_embedded_resource(response[field], rel)
                elif '_items' in response:
                    for item in response['_items']:
                        if field in item:
                            item[field] = _get_embedded_resource(item[field], rel)

                payload.data = json.dumps(response)


@trace
def _get_embedded_resource(external_id, rel):
    if not settings.hypermea.gateway_url:
        return

    url = f'{get_href_from_gateway(rel)}/{external_id}'
    auth = request.headers.get('Authorization')
    auth_header = {}
    if auth:
        auth_header = {
            'Authorization': auth
        }
    response = requests.get(url, headers=auth_header)
    # ASSERT: ok

    return {
        "_external": {
            "id": external_id,
            "rel": rel,
            "href": url
        },
        **response.json()
    }
