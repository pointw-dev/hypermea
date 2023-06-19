import logging
import json
import re
from utils import echo_message
import hooks._gateway
import hooks._error_handlers
import hooks._settings
import hooks._logs
from log_trace.decorators import trace
from configuration import SETTINGS

LOG = logging.getLogger('hooks')


@trace
def add_hooks(app):
    app.on_post_GET += _fix_links
    app.on_post_PATCH += _fix_links
    app.on_post_POST += _tidy_post_links

    if SETTINGS.has_enabled('HY_ADD_ECHO'):
        @app.route('/_echo', methods=['PUT'])
        def _echo_message():
            return echo_message()

    hooks._gateway.add_hooks(app)
    hooks._error_handlers.add_hooks(app)
    hooks._settings.add_hooks(app)
    hooks._logs.add_hooks(app)


@trace
@trace
def _tidy_post_links(resource, request, payload):
    if payload.status_code == 201:
        document = json.loads(payload.data)
        if '_items' in document:
            for item in document['_items']:
                _remove_unnecessary_links(links=item.get('_links', {}))
        else:
            _remove_unnecessary_links(links=document.get('_links', {}))

        if 'pretty' in request.args:
            payload.data = json.dumps(document, indent=4)
        else:
            payload.data = json.dumps(document)


@trace
def _fix_links(resource, request, payload):
    if payload.status_code in [200, 201]:
        document = json.loads(payload.data)

        if resource is None and '_links' in document:
            document['_links'] = _rewrite_schema_links(links=document.get('_links', {}))
        else:
            if '_items' in document:
                for item in document['_items']:
                    _process_item_links(links=item.get('_links', {}))
            else:
                _add_parent_link(links=document.get('_links', {}), resource=resource)
            _process_item_links(links=document.get('_links', {}))

        payload.data = json.dumps(document, indent=4 if 'pretty' in request.args else None)


@trace
def _process_item_links(links):
    if not links:
        return

    _remove_unnecessary_links(links)

    for link in links.values():
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
def _add_missing_slashes(link):
    href = link.get('href')
    if href and not (href.startswith('/') or href.startswith('http://') or href.startswith('https://')):
        link['href'] = '/' + href


@trace
def _insert_base_url(link):
    base_url = SETTINGS.get('HY_BASE_URL', '')
    if link['href'].startswith('/'):
        link['href'] = f'{base_url}{link["href"]}'


@trace
def _remove_regex_from_href(link):
    # TODO: this is needed due to a bug in Eve - fix that bug!
    if '<regex' in link['href']:
        link['href'] = re.sub('\/\<regex.*?\>', '', link['href'])


@trace
def _rewrite_schema_links(links):
    if not links or 'child' not in links or len(links) != 1:
        return

    old = links['child']
    del links['child']

    base_url = SETTINGS.get('HY_BASE_URL', '')

    new_links = {
        'self': {'href': f'{base_url}/', 'title': 'endpoints'},
        'logging': {'href': f'{base_url}/_logging', 'title': 'logging'}
    }

    for link in old:
        if '<' in link['href'] or link['title'] == '_schema':
            continue

        rel = link['title'][1:] if link['title'].startswith('_') else link['title']
        link['href'] = f'{base_url}/{link["href"]}'
        new_links[rel] = link

    return new_links


@trace
def _add_parent_link(links, resource):
    if not links or 'collection' not in links:
        return

    links['parent'] = {
        'href': links['collection']['href'],
        'title': resource
    }
