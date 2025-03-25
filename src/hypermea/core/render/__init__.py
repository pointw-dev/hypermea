import json
import requests
from flask import request, current_app
from eve.render import JSONRenderer
from hypermea.core.utils import get_api


class HALRenderer(JSONRenderer):
    mime = ("application/hal+json",)

    def render(self, data):
        self._check_for_embedded(data)
        return super(HALRenderer, self).render(data)

    def _check_for_embedded(self, data):
        embed_keys = request.args.getlist("embed")
        if not embed_keys:
            return

        if "_items" in data:
            # GET /resource (Eve paginated collection)
            for item in data["_items"]:
                self._embed_resources(item, embed_keys)
        elif isinstance(data, list):
            # Document list (GET /resource)
            for item in data:
                self._embed_resources(item, embed_keys)
        elif isinstance(data, dict):
            # Single document (GET /resource/{id})
            self._embed_resources(data, embed_keys)

    def _embed_resources(self, document, embed_keys):
        for embed_key in embed_keys:
            if "_embedded" in document and embed_key in document["_embedded"]:
                continue  # Already embedded

            href = self._get_href_to_embed(document, embed_key)
            if not href:
                continue

            embedded_data = self._fetch_embedded_data(href)
            if not embedded_data:
                continue

            try:
                self._add_embedded_section_to_document(document, embed_key, embedded_data)
            except Exception as e:
                current_app.logger.warning(f"Failed to embed {embed_key}: {e}")

    @staticmethod
    def _add_embedded_section_to_document(document, embed_key, embedded_data):
        if "_embedded" not in document:
            document["_embedded"] = {}
        if isinstance(embedded_data, dict) and "_items" in embedded_data:
            document["_embedded"][embed_key] = embedded_data["_items"]

            # Also propagate pagination links if they exist
            pagination_links = ["next", "prev", "last", "first"]
            for rel in pagination_links:
                page_link = embedded_data.get("_links", {}).get(rel)
                if page_link:
                    if "_links" not in document:
                        document["_links"] = {}
                    document["_links"][f"{embed_key}:{rel}"] = page_link
        else:
            document["_embedded"][embed_key] = embedded_data

    @staticmethod
    def _fetch_embedded_data(api_client, href):
        headers = {
            "Accept": "application/hal+json, application/json;q=0.9, */*;q=0"
        }

        if href.startswith("http"):
            resp = requests.get(href, headers=headers)
            embedded_data = resp.json()
        else:
            api_client = get_api()
            resp = api_client.get(href, headers=headers)
            embedded_data = resp.json

        if not resp.status_code == 200:
            embedded_data = None
        return embedded_data

    @staticmethod
    def _get_href_to_embed(document, embed_key):
        link_info = document.get("_links", {}).get(embed_key)
        if not link_info:
            # Detect parent relation
            parent_link = document.get("_links", {}).get("parent")
            if parent_link and parent_link.get("href", "/").lstrip("/").startswith(embed_key):
                link_info = parent_link
        href = link_info.get("href")
        return href
