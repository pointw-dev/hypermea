"""
Defines custom validations used in domain.
HypermeaValidator defines the following validations and types:

validations:
  unique_ignorecase
  unique_to_parent
  remote_relation

types:
  iso_date
  iso_time
  iso_duration
"""
import re
import logging

from eve.utils import config
from bson.objectid import ObjectId

from hypermea.core.utils import get_db
from hypermea.core.logging import trace
from hypermea.core.validation import HypermeaValidator

LOG = logging.getLogger('validator')


class CustomHypermeaValidator(HypermeaValidator):
    """
    add a custom validation by defining a method that starts with _validate_{your_validation_name}(self, {your_validation_name}, field, value):
        do nothing if the validation of the value passes validation for field, else call self._error(field, {message})
    add a custom type by defining a method that starts with _validate_type_{your_type_name}(self, value):
        return True if value correctly conforms to the type you want to create
    """
    pass
