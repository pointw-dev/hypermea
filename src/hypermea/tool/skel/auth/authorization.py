"""
The auth module used for HY.
"""
from bson.objectid import ObjectId
from hypermea_negotiable_auth import NegotiableAuth, AUTH_PARSER

from hypermea.core.utils import get_db
from . import SETTINGS
from .auth_handlers import basic, bearer, bearer_challenge

AUTH_PARSER.add_handler('Bearer', bearer, bearer_challenge, realm=f'{SETTINGS["AUTH_REALM"]}')
if SETTINGS.has_enabled('AUTH_ADD_BASIC'):
    AUTH_PARSER.add_handler('Basic', basic, realm=f'{SETTINGS["AUTH_REALM"]}')


class HypermeaAuthorization(NegotiableAuth):
    def __init__(self):
        super(HypermeaAuthorization, self).__init__()

    def authorized(self, allowed_roles, resource, method):
        get_home_allowed = SETTINGS.has_enabled('AUTH_ALLOW_GET_HOME') or SETTINGS.get('HY_GATEWAY_URL', False)
        if get_home_allowed and method == 'GET' and resource is None:
            return True

        return super().authorized(allowed_roles, resource, method)

    def process_claims(self, claims, allowed_roles, resource, method):
        authorized = "user" in claims and "permissions" in claims
        if not authorized:
            return False

        if method == 'HEAD':
            return True

        is_admin = claims.get('role') == 'admin'

        if not is_admin:
            auth_value = 'all-denied'
            accounts = get_db()['accounts']
            account = accounts.find_one({'user_id': claims['user']})
            if account:
                auth_value = ObjectId(account['_customer_ref'])
                claims['role'] = auth_value

            self.set_request_auth_value(auth_value)

        if resource in ['accounts', 'roles'] and not is_admin:
            authorized = False

        # NOTE: To set the tenant value, pass it to self.set_request_auth_value(), for example:
        # tenent_field = 'replace this with the name of the field'
        # tenent = claims[tenent_field].upper() if tenent_field in claims else 'unknown'
        # self.set_request_auth_value(tenent)

        return authorized
