import re
import json
import requests
from flask import request, current_app
from eve.render import JSONRenderer
from hypermea.core.render.context import HalResourceContext
from hypermea.core.utils import get_api, get_my_base_url, get_id_field, get_resource_id, clean_href, add_search_link, get_resource_rel


class HALRenderer(JSONRenderer):
    mime = ('application/hal+json',)


    def render(self, data):
        if '_error' in data:
            return super(HALRenderer, self).render(HALRenderer._halify_error(data))

        # set stage (context)
        self.data = data
        self.query_args = request.args

        self.resource = HalResourceContext.from_request(self.data)

        # action
        self._handle_links_only()
        self._add_links()
        self._handle_embed_query_string()

        if request.method == 'GET':
            self._move_items_to_embedded()

        return super(HALRenderer, self).render(self.data)

    def _handle_links_only(self):
        if 'links_only' in self.query_args:
            self.data.pop('_items')

    def _add_links(self):
        if self.resource.scope == 'item':
            self._add_links_to_item(self.data)
        if self.resource.scope == 'collection':
            self._add_links_to_collection()

    def _add_links_to_collection(self):
        if '_items' in self.data:
            for item in self.data['_items']:
                self._add_links_to_item(item)

        self_href = f'{self.resource.base_url}/{self.resource.name}'
        if '_links' not in self.data:
            self.data['_links'] = {
                'self': {
                    'href': self_href
                }
            }

        for rel in ['self', 'prev', 'next', 'last']:
            if rel in self.data['_links']:
                self.data['_links'][rel]['href'] = clean_href(self.data['_links'][rel]['href'])

        id_field = self.resource.id_field
        if id_field.startswith('_'):
            id_field = id_field[1:]

        self.data['_links'].update({
            'item': {
                'href': f'{self_href}/{{{id_field}}}',
                'templated': True
            },
            'search': add_search_link(self_href)
        })

    def _add_links_to_item(self, item):
        self.item_id = get_resource_id(item, self.resource.name)

        self._add_self_link(item)
        self._add_child_link(item)
        self._add_parent_links(item)


    def _add_self_link(self, item):
        # add link to myself
        item['_links']['self'] = {
            'href': f"{self.resource.base_url}/{self.resource.name}/{self.item_id}"
        }

    def _add_child_link(self, item):
        # add child link if I am a parent to someone
        for resource in self.resource.domain.keys():
            if '_' not in resource:
                continue
            parent, child = resource.split('_')
            rel = get_resource_rel(child)
            if parent == self.resource.name:
                item['_links'][rel] = {
                    'href': f'{self.resource.base_url}/{self.resource.name}/{self.item_id}/{child}',
                }

    def _add_parent_links(self, item):
        # add any parent links if I am a child to anyone
        parent_rel = ''

        for field, spec in [spec for spec in self.resource.schema.items() if 'data_relation' in spec[1]]:
            parent = spec['data_relation'].get('resource')
            parent_rel = parent if parent_rel else 'parent'  # if there are multiples, the first is "parent"
            if parent:
                if field in item:
                    parent_id = item[field]
                else:
                    parent_id = request.view_args.get(field)
                item['_links']['parent'] = {
                    'href': f'{self.resource.base_url}/{parent}/{parent_id}',
                }
                if parent_rel == 'parent':
                    item['_links']['collection'] = {
                        'href': f'{self.resource.base_url}/{parent}/{parent_id}/{self.resource.name}',
                    }
        if not parent_rel:
            collection_href = f'{self.resource.base_url}/{self.resource.name}'
            item['_links']['parent'] = {
                'href': collection_href
            }
            item['_links']['collection'] = {
                'href': collection_href
            }


    def _move_items_to_embedded(self):
        items = self.data.pop('_items', None)
        if items is not None:
            embedded = self.data.setdefault('_embedded', {})
            embedded[self.resource.rel] = items

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

    def _get_href_to_embed(self, document, embed_key):
        link_info = document.get('_links', {}).get(embed_key)
        if not link_info:
            parent_link = None
            # Detect parent relation
            for field, spec in [spec for spec in self.resource.schema.items() if 'data_relation' in spec[1]]:
                parent_resource_name = spec['data_relation'].get('resource')
                parent_rel = get_resource_rel(parent_resource_name)
                if parent_rel == embed_key:
                    parent_link = document.get('_links', {}).get('related',{}).get(field)
                break

            if parent_link:
                link_info = parent_link

        if not link_info:
            return None

        href = link_info.get('href')
        return href


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
    def _halify_error(data):
        rtn = {
            'status': data.get('_status',"unknown"),
            'status_code': data['_error']['code'],
            'message': data['_error']['message'],
            '_links': {
                "self": request.url
            }
        }

        if '_issues' in data:
            rtn['_embedded'] = {
                "issues": data['_issues']
            }

        return rtn
