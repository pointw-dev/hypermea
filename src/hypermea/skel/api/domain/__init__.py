"""
Defines the resources that comprise the {$project_name} domain.
"""
from . import _settings
from ._common import OBJECT_ID_REGEX


DOMAIN_DEFINITIONS = {
    '_settings': _settings.DEFINITION
}


DOMAIN_RELATIONS = {
}


DOMAIN = {**DOMAIN_DEFINITIONS, **DOMAIN_RELATIONS}
