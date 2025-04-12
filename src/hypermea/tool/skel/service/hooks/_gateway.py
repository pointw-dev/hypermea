"""
hooks._gateway
This module defines hooks the request chain to the appropriate gateway utils
"""
import logging
from hypermea.core.logging import trace
from hypermea.core.gateway import handle_post_from_remote, embed_remote_parent_resource

LOG = logging.getLogger('hooks.gateway')


@trace
def add_hooks(app):
    app.on_post_GET += embed_remote_parent_resource
    app.on_pre_POST += handle_post_from_remote
