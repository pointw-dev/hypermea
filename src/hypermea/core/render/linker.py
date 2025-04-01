from flask import request, current_app
from hypermea.core.utils import clean_href, add_search_link, get_resource_id, get_resource_rel


class HalLinker:
    def __init__(self, resource):
        self.item_id = None
        self.resource = resource


    def process_links(self, data):
        if 'links_only' in self.resource.query_args:
            data.pop('_items')

        if self.resource.scope == 'item':
            self.add_links_to_item(data)
        if self.resource.scope == 'collection':
            self.add_links_to_collection(data)






    def add_links_to_item(self, item):
        self.item_id = get_resource_id(item, self.resource.name)

        self._add_self_link(item)
        self._add_child_link(item)
        self._add_parent_links(item)

    def add_links_to_collection(self, data):
        if '_items' in data:
            for item in data['_items']:
                self.add_links_to_item(item)

        self_href = f'{self.resource.base_url}/{self.resource.name}'
        data['_links'] = data.get('_links', {})
        data['_links']['self'] = {
            'href': self_href
        }

        for rel in ['self', 'prev', 'next', 'last']:
            if rel in data['_links']:
                data['_links'][rel]['href'] = clean_href(data['_links'][rel]['href'])

        id_field = self.resource.id_field
        if id_field.startswith('_'):
            id_field = id_field[1:]

        data['_links'].update({
            'item': {
                'href': f'{self_href}/{{{id_field}}}',
                'templated': True
            },
            'search': add_search_link(self_href)
        })

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
