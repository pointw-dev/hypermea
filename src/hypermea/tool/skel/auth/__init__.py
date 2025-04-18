"""Home of the auth modules that govern access to hypermea resources and other endpoints."""
import os
import logging
import jwt
import settings

LOG = logging.getLogger('auth')

try:
    JWK_CLIENT = jwt.PyJWKClient(f'https://{settings.auth.jwt_domain}/.well-known/jwks.json')
    _jwks = JWK_CLIENT.get_signing_keys()
    SIGNING_KEYS = {jwk.key_id: jwk.key for jwk in _jwks}
except jwt.exceptions.PyJWKClientError:
    LOG.warning('The auth addin is installed but not properly configured.')
    SIGNING_KEYS = {}
