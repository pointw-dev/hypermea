from flask import request, current_app
from hypermea.core.href import clean_href, add_search_link, get_resource_id, get_resource_rel, get_my_base_url, \
    get_self_href_from_request, url_join
from hypermea.core.gateway import get_href_from_gateway
import settings


class HalLinker:
    def __init__(self, resource):
        self.item_id = None
        self.resource = resource


    def process_links(self, data):
        if 'links_only' in self.resource.query_args:
            data.pop('_items')

        if self.resource.name == 'home' and self.resource.scope == 'root':
            data['_links'] = HalLinker._rewrite_home_resource_links(data['_links'])
            return

        HalLinker._remove_unnecessary_links(links=data.get('_links', {}))
        if '_items' in data:
            for item in data['_items']:
                HalLinker._remove_unnecessary_links(links=item.get('_links', {}))

        if self.resource.scope == 'generated':
            data['_links'] = {
                'self': {
                    'href': f'{self.resource.base_url}/{self.resource.name}'
                }
            }
        elif self.resource.scope == 'item':
            self._add_links_to_item(data)
        elif self.resource.scope == 'collection':
            self._add_links_to_collection(data)

    def _add_links_to_item(self, item):
        if not item:
            return

        self.item_id = get_resource_id(item, self.resource.name)

        self._add_self_link(item)
        self._add_child_link(item)
        self._add_parent_links(item)

    def _add_links_to_collection(self, data):
        if '_items' in data:
            for item in data['_items']:
                self._add_links_to_item(item)


        self_href = get_self_href_from_request()
        data['_links'] = data.get('_links', {})
        data['_links']['self'] = {
            'href': self_href
        }
        self._add_parent_links(data)

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
        item['_links']['self'] = {
            'href': f'{self.resource.base_url}/{self.resource.name}/{self.item_id}'
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
        added_parent_link = False
        parent_resource_name = 'n/a'
        for field, spec in [spec for spec in self.resource.schema.items() if ('data_relation' in spec[1] or 'external_relation' in spec[1])]:
            if 'data_relation' in spec:
                parent_resource_name = spec['data_relation'].get('resource')
                parent_rel = get_resource_rel(parent_resource_name)
            else:
                parent_rel = spec['external_relation'].get('rel')

            if parent_rel:
                if field in item:
                    parent_id = str(item[field])
                else:
                    parent_id = str(request.view_args.get(field))

                base_href = f'{self.resource.base_url}/{parent_resource_name}' if 'data_relation' in spec else get_href_from_gateway(parent_rel)
                href = url_join(base_href, parent_id)
                item['_links'][parent_rel] = {
                    'href': href,
                }
                if not added_parent_link:
                    item['_links']['parent'] = {
                        'href': href,
                    }
                    item['_links']['collection'] = {
                        'href': f'{href}/{self.resource.name}',
                    }
                    added_parent_link = True

        if not added_parent_link:
            collection_href = f'{self.resource.base_url}/{self.resource.name}'
            item['_links']['parent'] = {
                'href': collection_href
            }
            item['_links']['collection'] = {
                'href': collection_href
            }

    @staticmethod
    def _remove_unnecessary_links(links):
        if not links:
            return
        links.pop('related', None)


    @staticmethod
    def _rewrite_home_resource_links(links):
        if not links or 'child' not in links or len(links) != 1:
            return

        old = links.pop('child')
        base_url = get_my_base_url()

        new_links = {
            'self': {'href': f'{base_url}/', '_note': f'Home resource for {settings.hypermea.service_name}'},
            'logging': {'href': f'{base_url}/_logging', '_note': 'logging verbosity: GET, PUT'},
            'settings': {'href': f'{base_url}/_settings', '_note': 'versions and settings: GET'},
        }

        for link in old:
            if '<' in link['href'] or link['title'] == '_schema':
                continue

            add_links_only = False
            if link['title'].startswith('_'):
                rel = link['title'][1:]
            else:
                rel = get_resource_rel(link['title'])
                add_links_only = True

            link['href'] = f'{base_url}/{link["href"]}'
            if add_links_only:
                #115, disabling this for now - may have setting to re-enable
                    # link['href'] += '{?links_only}'
                    # link['templated'] = True
                link['_note'] = 'add ?links_only query string to GET _links without the collection'
            link.pop('title', None)
            new_links[rel] = link

        return new_links
