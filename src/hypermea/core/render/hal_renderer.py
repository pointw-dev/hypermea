from flask import request, current_app
from eve.render import JSONRenderer
from hypermea.core.utils import get_api, get_my_base_url, get_id_field, get_resource_id, clean_href, add_search_link, \
    get_resource_rel, hal_format_error
from hypermea.core.render.context import ResourceContext
from hypermea.core.render.linker import HalLinkBuilder
from hypermea.core.render.embedder import HalEmbedder


class HALRenderer(JSONRenderer):
    mime = ('application/hal+json',)

    def __init__(self):
        self.data = None
        self.query_args = None
        self.resource = None
        self.link_builder = None
        self.embedder = None

    def render(self, data):
        if '_error' in data:
            return super(HALRenderer, self).render(hal_format_error(data))

        # set stage (context)
        self.data = data
        self.resource = ResourceContext.from_request(self.data)
        self.link_builder = HalLinkBuilder(self.resource)
        self.embedder = HalEmbedder(self.resource)

        # action
        self._handle_links_only()
        self._add_links()
        self.embedder.handle_embed_query_string(self.data)

        if request.method == 'GET':
            self.embedder.move_items_to_embedded(self.data)

        return super(HALRenderer, self).render(self.data)

    def _handle_links_only(self):
        if 'links_only' in self.resource.query_args:
            self.data.pop('_items')

    def _add_links(self):
        if self.resource.scope == 'item':
            self.link_builder.add_links_to_item(self.data)
        if self.resource.scope == 'collection':
            self.link_builder.add_links_to_collection(self.data)
