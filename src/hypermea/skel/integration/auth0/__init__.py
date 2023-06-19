"""
Methods to access/modify user information in Auth0
https://auth0.com/docs/api/management/v2
"""
import logging
import json
import requests
from log_trace.decorators import trace
from configuration import SETTINGS

LOG = logging.getLogger('{$integration}')

SETTINGS.set_prefix_description('{$prefix}', 'Auth0 configuration')
SETTINGS.create('{$prefix}', {
    'API_AUDIENCE': 'https://{$project_name}.us.auth0.com/api/v2/',
    'API_BASE_URL': 'https://{$project_name}.us.auth0.com/api/v2',
    'CLAIMS_NAMESPACE': 'https://pointw.com/{$project_name}',
    'TOKEN_ENDPOINT': 'https://{$project_name}.us.auth0.com/oauth/token',
    'CLIENT_ID': '--your-client-id--',
    'CLIENT_SECRET': '--your-client-secret--'
})


@trace
def get_token():
    token_url = SETTINGS['{$prefix}_TOKEN_ENDPOINT']
    client_id = SETTINGS['{$prefix}_CLIENT_ID']
    client_secret = SETTINGS['{$prefix}_CLIENT_SECRET']
    audience = SETTINGS['{$prefix}_API_AUDIENCE']

    body = json.dumps({
        'client_id': client_id,
        'client_secret': client_secret,
        'audience': audience,
        'grant_type': 'client_credentials'
    })
    headers = {
        'content-type': 'application/json'
    }
    response = requests.post(token_url, headers=headers, data=body)
    # TODO: robustify
    token = response.json()['access_token']
    return token


@trace
def get_users(token):
    get_users_url = f'{SETTINGS["{$prefix}_API_BASE_URL"]}/users'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.get(get_users_url, headers=headers)
    return response.json()


@trace
def get_user_roles(user_id, token):
    get_roles_url = f'{SETTINGS["{$prefix}_API_BASE_URL"]}/users/{user_id}/roles'

    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.get(get_roles_url, headers=headers)
    # TODO: robustify
    return response.json()


@trace
def add_user_roles(token, user_id, roles_to_add, remove=False):
    # TODO: refactor ugly bad handling
    # NOTE: role names are case sensitive
    get_roles_url = f'{SETTINGS["{$prefix}_API_BASE_URL"]}/roles'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-type': 'application/json'
    }
    response = requests.get(get_roles_url, headers=headers)
    roles = response.json()
    role_ids = [role['id'] for role in roles if role['name'] in roles_to_add]

    request_body = {
        'roles': role_ids
    }
    if role_ids:
        user_roles_url = f'{SETTINGS["{$prefix}_API_BASE_URL"]}/users/{user_id}/roles'
        if remove:
            response = requests.delete(user_roles_url, headers=headers, data=json.dumps(request_body))
        else:
            response = requests.post(user_roles_url, headers=headers, data=json.dumps(request_body))
        LOG.info(f'{"Removed" if remove else "Added"} roles on {user_id}: {response.status_code}')
        if response.status_code != 204:
            return False
    else:
        LOG.warning('no valid roles specified')
        return False

    return True


@trace
def delete_user(token, user_id):
    user_url = f'{SETTINGS["{$prefix}_API_BASE_URL"]}/users/{user_id}'
    headers = {
        'Authorization': 'Bearer ' + token
    }
    response = requests.delete(user_url, headers=headers)

    LOG.info(f'"Removed {user_id} from auth0: {response.status_code}')
    return response.status_code == 204
