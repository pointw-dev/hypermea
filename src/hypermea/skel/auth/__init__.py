"""Home of the auth modules that govern access to hypermea resources (and other endpoints)."""
import os
import logging
import jwt
from configuration import SETTINGS

LOG = logging.getLogger('auth')

SETTINGS.set_prefix_description('AUTH', 'HypermeaService authorization settings')
SETTINGS.create('AUTH', {
    'ADD_BASIC': 'No',  # [0] in 'yYtT', i.e. yes, Yes, true, True
    'ROOT_PASSWORD': 'password',
    'REALM': '{$project_name}.hypermea.com',
    "CLAIMS_NAMESPACE": "uri://hypermea.com/claims",

    'JWT_DOMAIN': '{$project_name}.us.auth0.com',
    'JWT_ISSUER': 'https://{$project_name}.us.auth0.com/',
    'JWT_AUDIENCE': 'uri://hypermea.com/{$project_name}'
})

SETTINGS.create('AUTH', 'ENABLE_ROOT_USER', is_optional=True)
SETTINGS.create('AUTH', 'ALLOW_GET_HOME', is_optional=True)

try:
    JWK_CLIENT = jwt.PyJWKClient(f'https://{SETTINGS["AUTH_JWT_DOMAIN"]}/.well-known/jwks.json')
    _jwks = JWK_CLIENT.get_signing_keys()
    SIGNING_KEYS = {jwk.key_id: jwk.key for jwk in _jwks}
except jwt.exceptions.PyJWKClientError:
    LOG.warning('The auth addin is installed but not properly configured.')
    SIGNING_KEYS = {}

## # cancellable
## if SETTINGS['AUTH_JWT_AUDIENCE'] == '':
##     del SETTINGS['AUTH_JWT_AUDIENCE']
