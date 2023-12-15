"""
hooks._gateway
This module defines hooks the request chain to the appropriate gateway utils
"""
import logging
from hypermea.logging import trace
from hypermea.gateway import _handle_post_from_remote, _embed_remote_parent_resource

LOG = logging.getLogger('hooks.gateway')


@trace
def add_hooks(app):
    app.on_post_GET += _embed_remote_parent_resource
    app.on_pre_POST += _handle_post_from_remote
