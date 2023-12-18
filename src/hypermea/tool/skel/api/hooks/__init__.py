import logging
from hypermea.core.hooks import fix_links, tidy_post_links
from hypermea.core.utils import echo_message
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
    app.on_post_GET += fix_links
    app.on_post_PATCH += fix_links
    app.on_post_POST += tidy_post_links

    affordances.rfc6861.create_form.add_affordance(app)
    affordances.rfc6861.edit_form.add_affordance(app)

    if SETTINGS.has_enabled('HY_ADD_ECHO'):
        @app.route('/_echo', methods=['PUT'])
        def _echo_message():
            return echo_message()

    hooks._gateway.add_hooks(app)
    hooks._error_handlers.add_hooks(app)
    hooks._settings.add_hooks(app)
    hooks._logs.add_hooks(app)
