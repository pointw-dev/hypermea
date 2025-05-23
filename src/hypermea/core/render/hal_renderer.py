from eve.render import JSONRenderer
from hypermea.core.response import hal_format_error
from hypermea.core.render.context import ResourceContext
from hypermea.core.render.linker import HalLinker
from hypermea.core.render.embedder import HalEmbedder


class HALRenderer(JSONRenderer):
    mime = ('application/hal+json',)

    def render(self, data):
        if '_error' in data:
            return super(HALRenderer, self).render(hal_format_error(data))

        resource = ResourceContext.from_request(data)
        HalLinker(resource).process_links(data)
        HalEmbedder(resource).process_embedding(data)

        return super(HALRenderer, self).render(data)
