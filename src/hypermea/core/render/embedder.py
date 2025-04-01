import requests
from flask import current_app
from hypermea.core.utils import get_resource_rel, get_api


class HalEmbedder:
    def __init__(self, resource):
        self.resource = resource

    def process_embedding(self, data):
        self.handle_embed_query_string(data)
        if self.resource.method == 'GET':
            self.move_items_to_embedded(data)





    def handle_embed_query_string(self, data):
        embed_keys = self.resource.query_args.getlist('embed')
        if not embed_keys:
            return

        if '_items' in data:
            # GET /resource (Eve paginated collection)
            for item in data['_items']:
                self._embed_resources(item, embed_keys)
        elif isinstance(data, list):
            # Document list (GET /resource)
            for item in data:
                self._embed_resources(item, embed_keys)
        elif isinstance(data, dict):
            # Single document (GET /resource/{id})
            self._embed_resources(data, embed_keys)

    def move_items_to_embedded(self, data):
        items = data.pop('_items', None)
        if items is not None:
            embedded = data.setdefault('_embedded', {})
            embedded[self.resource.rel] = items


    def _embed_resources(self, document, embed_keys):
        for embed_key in embed_keys:
            if '_embedded' in document and embed_key in document['_embedded']:
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
                current_app.logger.warning(f'Failed to embed {embed_key}: {e}')

    def _get_href_to_embed(self, document, embed_key):
        link_info = document.get('_links', {}).get(embed_key)
        if not link_info:
            parent_link = None
            # Detect parent relation
            for field, spec in [spec for spec in self.resource.schema.items() if 'data_relation' in spec[1]]:
                parent_resource_name = spec['data_relation'].get('resource')
                parent_rel = get_resource_rel(parent_resource_name)
                if parent_rel == embed_key:
                    parent_link = document.get('_links', {}).get('related', {}).get(field)
                break

            if parent_link:
                link_info = parent_link

        if not link_info:
            return None

        href = link_info.get('href')
        return href


    @staticmethod
    def _fetch_embedded_data(href):
        headers = {
            'Accept': 'application/hal+json, application/json;q=0.9, */*;q=0'
        }

        if href.startswith('http'):
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
    def _add_embedded_section_to_document(document, embed_key, embedded_data):
        if '_embedded' not in document:
            document['_embedded'] = {}

        if '_embedded' in embedded_data and embed_key in embedded_data['_embedded']:
            embedded_links = embedded_data['_links']
            document['_embedded'][embed_key] = embedded_data['_embedded'].pop(embed_key, {})
            pagination_links = ['next', 'prev', 'last', 'first']
            for rel in pagination_links:
                page_link = embedded_links.get(rel)
                if page_link:
                    if '_links' not in document:
                        document['_links'] = {}
                    document['_links'][f'{embed_key}:{rel}'] = page_link
            return

        document['_embedded'][embed_key] = embedded_data
