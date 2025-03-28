import json
import requests
from flask import request, current_app
from eve.render import JSONRenderer
from hypermea.core.utils import get_api, get_my_base_url, get_id_field, get_resource_id, clean_href, add_search_link


class HALRenderer(JSONRenderer):
    mime = ('application/hal+json',)


    def render(self, data):
        self.data = data
        self.query_args = request.args
        self.resource_name, self.resource_scope = HALRenderer._parse_url_rule()
        if '_' in self.resource_name:
            self.parent, self.child = self.resource_name.split('_', 1)
            self.resource_name = self.child
        self.base_url = get_my_base_url()
        self.id_field = get_id_field(self.resource_name)
        self.domain = current_app.config['DOMAIN']
        self.schema = self.domain.get(self.resource_name, {}).get('schema')

        self._handle_links_only()
        self._add_links()
        self._handle_embed_query_string()

        if request.method == 'GET':
            self._move_items_to_embedded()

        return super(HALRenderer, self).render(self.data)


    def _handle_links_only(self):
        if 'links-only' in self.query_args:
            self.data.pop('_items')

    def _add_links(self):
        if self.resource_scope == 'item':
            self._add_links_to_item(self.data)
        if self.resource_scope == 'collection':
            self._add_links_to_collection()

    def _add_links_to_item(self, item):
        self.item_id = get_resource_id(item, self.resource_name)

        self._add_self_link(item)
        self._add_child_link(item)
        self._add_parent_links(item)

    def _add_links_to_collection(self):
        if '_items' in self.data:
            for item in self.data['_items']:
                self._add_links_to_item(item)


        self_href = f'{self.base_url}/{self.resource_name}'
        if '_links' not in self.data:
            self.data['_links'] = {
                'self': {
                    'href': self_href
                }
            }

        for rel in ['self', 'prev', 'next', 'last']:
            if rel in self.data['_links']:
                self.data['_links'][rel]['href'] = clean_href(self.data['_links'][rel]['href'])

        id_field = self.id_field
        if id_field.startswith('_'):
            id_field = id_field[1:]

        self.data['_links'].update({
            'item': {
                'href': f'{self_href}/{{{id_field}}}',
                'templated': True
            },
            'search': add_search_link(self_href)
        })


    def _add_self_link(self, item):
        # add link to myself
        item['_links']['self'] = {
            'href': f"{self.base_url}/{self.resource_name}/{self.item_id}"
        }

    def _add_child_link(self, item):
        # add child link if I am a parent to someone
        for resource in self.domain.keys():
            if '_' not in resource:
                continue
            parent, child = resource.split('_')
            if parent == self.resource_name:
                item['_links'][child] = {
                    'href': f'{self.base_url}/{self.resource_name}/{self.item_id}/{child}',
                }

    def _add_parent_links(self, item):
        # add any parent links if I am a child to anyone
        parent_rel = ''
#        for field, spec in self.schema.items():
#            if 'data_relation' in spec:
        for field, spec in [spec for spec in self.schema.items() if 'data_relation' in spec[1]]:
            parent = spec['data_relation'].get('resource')
            parent_rel = parent if parent_rel else 'parent'  # if there are multiples, the first is "parent"
            if parent:
                item['_links']['parent'] = {
                    'href': f'{self.base_url}/{parent}/{item[field]}',
                }
                if parent_rel == 'parent':
                    item['_links']['collection'] = {
                        'href': f'{self.base_url}/{parent}/{item[field]}/{self.resource_name}',
                    }
        if not parent_rel:
            collection_href = f'{self.base_url}/{self.resource_name}' 
            item['_links']['parent'] = {
                'href': collection_href
            }
            item['_links']['collection'] = {
                'href': collection_href
            }


    @staticmethod
    def _parse_url_rule():
        resource_name, scope = request.url_rule.endpoint.split('|')
        scope = {
            'resource': 'collection',
            'item_lookup': 'item'
        }.get(scope, scope)
        return resource_name, scope

    def _move_items_to_embedded(self):
        items = self.data.pop('_items', None)
        if items is not None:
            embedded = self.data.setdefault('_embedded', {})
            embedded[self.resource_name] = items

    def _handle_embed_query_string(self):
        embed_keys = self.query_args.getlist('embed')
        if not embed_keys:
            return

        if '_items' in self.data:
            # GET /resource (Eve paginated collection)
            for item in self.data['_items']:
                self._embed_resources(item, embed_keys)
        elif isinstance(self.data, list):
            # Document list (GET /resource)
            for item in self.data:
                self._embed_resources(item, embed_keys)
        elif isinstance(self.data, dict):
            # Single document (GET /resource/{id})
            self._embed_resources(self.data, embed_keys)

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
    def _get_href_to_embed(document, embed_key):
        link_info = document.get('_links', {}).get(embed_key)
        if not link_info:
            # Detect parent relation
            parent_link = document.get('_links', {}).get('related',{}).get(f'_{embed_key}_ref')
            if parent_link:
                link_info = parent_link

        if not link_info:
            return None

        href = link_info.get('href')
        return href
