import requests
from flask import current_app, request
from hypermea.core.utils import get_api
from hypermea.core.href import get_resource_rel, get_id_field, get_my_base_url


class HalEmbedder:
    def __init__(self, resource):
        self.resource = resource

    def process_embedding(self, data):
        self._handle_embed_query_string(data)
        if self.resource.method == 'GET':
            self._move_items_to_embedded(data)


    def _handle_embed_query_string(self, data):
        embed_rels = self.resource.query_args.getlist('embed')
        if not embed_rels:
            return

        if '_items' in data:
            for item in data['_items']:
                self._embed_resources(item, embed_rels)
        elif isinstance(data, list):
            for item in data:
                self._embed_resources(item, embed_rels)
        elif isinstance(data, dict):
            self._embed_resources(data, embed_rels)

    def _move_items_to_embedded(self, data):
        items = data.pop('_items', None)
        if items is not None:
            embedded = data.setdefault('_embedded', {})
            embedded[self.resource.rel] = items


    def _embed_resources(self, data, embed_rels):
        for embed_rel in embed_rels:
            if '_embedded' in data and embed_rel in data['_embedded']:
                continue  # Already embedded

            href = data.get('_links', {}).get(embed_rel, {}).get('href')
            if not href:
                continue

            embedded_data = self._fetch_embedded_data(href)
            if not embedded_data:
                continue

            try:
                self._add_embedded_section_to_data(data, embed_rel, embedded_data)
            except Exception as e:
                current_app.logger.warning(f'Failed to embed {embed_rel}: {e}')


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
    def _add_embedded_section_to_data(data, embed_rel, embedded_data):
        if '_embedded' not in data:
            data['_embedded'] = {}

        if '_embedded' in embedded_data and embed_rel in embedded_data['_embedded']:
            embedded_links = embedded_data['_links']
            data['_embedded'][embed_rel] = embedded_data['_embedded'].pop(embed_rel, {})
            pagination_links = ['next', 'prev', 'last', 'first']
            for pagination_rel in pagination_links:
                page_link = embedded_links.get(pagination_rel)
                if page_link:
                    if '_links' not in data:
                        data['_links'] = {}
                    data['_links'][f'{embed_rel}:{pagination_rel}'] = page_link
            return

        data['_embedded'][embed_rel] = embedded_data
