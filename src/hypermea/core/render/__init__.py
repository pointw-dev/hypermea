import json
from flask import request, current_app
from eve.render import JSONRenderer
from hypermea.core.utils import get_api


class HALRenderer(JSONRenderer):
    mime = ("application/hal+json",)

    def render(self, data):
        embed_keys = request.args.getlist("embed")

        if not embed_keys:
            return super(HALRenderer, self).render(data)

        if isinstance(data, dict):
            # Single document (GET /resource/{id})
            self._embed_resources(data, embed_keys)
        elif isinstance(data, list):
            # Document list (GET /resource)
            for item in data:
                self._embed_resources(item, embed_keys)
        elif "_items" in data:
            # GET /resource (Eve paginated collection)
            for item in data["_items"]:
                self._embed_resources(item, embed_keys)

        return super(HALRenderer, self).render(data)

    def _embed_resources(self, document, embed_keys):
        api_client = get_api()

        for embed_key in embed_keys:
            if "_embedded" in document and embed_key in document["_embedded"]:
                continue  # Already embedded

            link_info = document.get("_links", {}).get(embed_key)

            if not link_info:
                # Try to detect parent relation generically
                parent_link = document.get("_links", {}).get("parent")
                if parent_link and parent_link.get("href", "/").lstrip("/").startswith(embed_key):
                    link_info = parent_link
                else:
                    continue  # No suitable link found

            href = link_info.get("href")
            if not href:
                continue

            resp = api_client.get(href, headers={"Accept": "application/hal+json"})

            if resp.status_code == 200:
                try:
                    embedded_data = json.loads(resp.get_data(as_text=True))
                    if "_embedded" not in document:
                        document["_embedded"] = {}

                    if isinstance(embedded_data, dict) and "_items" in embedded_data:
                        document["_embedded"][embed_key] = embedded_data["_items"]

                        # Also propagate pagination links if they exist
                        pagination_links = ["next", "prev", "last", "first"]
                        for rel in pagination_links:
                            pagelink = embedded_data.get("_links", {}).get(rel)
                            if pagelink:
                                if "_links" not in document:
                                    document["_links"] = {}
                                document["_links"][f"{embed_key}:{rel}"] = pagelink
                    else:
                        document["_embedded"][embed_key] = embedded_data
                except Exception as e:
                    current_app.logger.warning(f"Failed to embed {embed_key}: {e}")
