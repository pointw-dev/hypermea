import logging
from hypermea.core.hooks import add_hypermea_hooks
from hypermea.core.logging import trace
import hooks._gateway
import hooks._error_handlers
import hooks._settings
import hooks._logs
import affordances
from configuration import SETTINGS

LOG = logging.getLogger('hooks')


@trace
def add_hooks(app):
    add_hypermea_hooks(app)

    affordances.rfc6861.create_form.add_affordance(app)
    affordances.rfc6861.edit_form.add_affordance(app)

    hooks._gateway.add_hooks(app)
    hooks._error_handlers.add_hooks(app)
    hooks._settings.add_hooks(app)
    hooks._logs.add_hooks(app)
