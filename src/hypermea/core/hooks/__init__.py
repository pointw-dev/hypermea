import logging
import json
import re
from hypermea.core.utils import get_my_base_url
from hypermea.core.logging import trace
from configuration import SETTINGS

@trace
def tidy_post_links(_, request, payload):
    if payload.status_code == 201:
        document = json.loads(payload.data)
        if '_items' in document:
            for item in document['_items']:
                _remove_unnecessary_links(links=item.get('_links', {}))
        else:
            _remove_unnecessary_links(links=document.get('_links', {}))

        payload.data = json.dumps(document, indent=4 if 'pretty' in request.args else None)


@trace
def fix_links(resource, request, payload):
    if payload.status_code in [200, 201]:
        document = json.loads(payload.data)

        if resource is None and '_links' in document:
            document['_links'] = _rewrite_schema_links(links=document.get('_links', {}))
        else:
            if '_' in resource:
                parent_resource, resource = resource.split('_', 1)
            collection = document.get('_embedded', {}).get(resource)
            if collection:
                for item in collection:
                    _process_item_links(links=item.get('_links', {}))
            _process_item_links(links=document.get('_links', {}))

        payload.data = json.dumps(document, indent=4 if 'pretty' in request.args else None)


@trace
def _process_item_links(links):
    if not links:
        return

    _remove_unnecessary_links(links)

    for link in links.values():
        _remove_title(link)
        _add_missing_slashes(link)
        _insert_base_url(link)
        _remove_regex_from_href(link)


@trace
def _remove_unnecessary_links(links):
    if not links:
        return

    if 'related' in links:
        del links['related']


@trace
def _remove_title(link):
    link.pop('title', None)


@trace
def _add_missing_slashes(link):
    href = link.get('href')
    if href and not (href.startswith('/') or href.startswith('http://') or href.startswith('https://')):
        link['href'] = '/' + href


@trace
def _insert_base_url(link):
    base_url = get_my_base_url()
    if link['href'].startswith('/'):
        link['href'] = f'{base_url}{link["href"]}'


@trace
def _remove_regex_from_href(link):
    # TODO: this is needed due to a bug in Eve - fix that bug!
    if '<regex' in link['href']:
        link['href'] = re.sub(r'\/\<regex.*?\>', '', link['href'])


@trace
def _rewrite_schema_links(links):
    if not links or 'child' not in links or len(links) != 1:
        return

    old = links['child']
    del links['child']

    base_url = get_my_base_url()

    new_links = {
        'self': {'href': f'{base_url}/', '_note': f'Root resource for {SETTINGS["HY_API_NAME"]}'},
        'logging': {'href': f'{base_url}/_logging'}
    }

    for link in old:
        if '<' in link['href'] or link['title'] == '_schema':
            continue

        add_links_only = False
        if link['title'].startswith('_'):
            rel = link['title'][1:]
        else:
            rel = link['title']
            add_links_only = True

        link['href'] = f'{base_url}/{link["href"]}'
        if add_links_only:
            link['href'] += '{?links-only}'
            link['templated'] = True
        link.pop('title', None)
        new_links[rel] = link

    return new_links


@trace
def _add_parent_link(links):
    if not links or 'collection' not in links:
        return

    links['parent'] = {
        'href': links['collection']['href']
    }
