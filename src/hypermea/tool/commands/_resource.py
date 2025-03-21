import glob
import os

import click

import hypermea.tool
from hypermea.tool.code_gen import DomainDefinitionInserter, HooksInserter, DomainResourceRemover, HooksRemover, \
    ParentReferenceRemover, ChildLinksRemover


def _create(resource_name, no_common):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    singular, plural = hypermea.tool.get_singular_plural(resource_name)
    if _is_resource_name_is_invalid(singular, plural):
        return hypermea.tool.escape(f'The resource name ({resource_name}) is invalid', 701)

    add_common = not no_common

    print(f'Creating {plural} resource')
    if _resource_already_exists(plural):
        hypermea.tool.escape('This resource already exist', 702)
    else:
        _create_resource_domain_file(plural, add_common)
        _insert_domain_definition(plural)
        _create_resource_hook_file(singular, plural)
        _insert_hooks(plural)

    hypermea.tool.jump_back_to(starting_folder)


def _list_resources():
    resources_list = _get_resource_list()
    for resource in resources_list:
        print('- ' + resource)


def _remove(resource_name):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    singular, plural = hypermea.tool.get_singular_plural(resource_name)
    if _is_resource_name_is_invalid(singular, plural):
        return hypermea.tool.escape(f'The resource name ({resource_name}) is invalid', 701)

    if not _resource_already_exists(plural):
        hypermea.tool.escape('This resource does not exist', 703)

    _remove_domain_definition(plural)
    _remove_hooks(plural)
    _delete_resource_files(plural)
    _remove_references_from_children(plural)
    _remove_child_links(plural)
    hypermea.tool.jump_back_to(starting_folder)


def _check(resource_name):
    singular, plural = hypermea.tool.get_singular_plural(resource_name)
    click.echo(f'You entered {resource_name}')
    click.echo(f'- singular: {singular}')
    click.echo(f'- plural:   {plural}')

    click.echo(f'A resource named {plural} ' +
               ('already exists' if _resource_already_exists(plural) else 'does not exist'))


def _resource_already_exists(resource_name):
    resources_list = _get_resource_list()
    return resource_name in resources_list


def _is_resource_name_is_invalid(singular, plural):
    # TODO: check validity of names
    return False


def _get_resource_list():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/domain')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    with open('__init__.py', 'r') as f:
        lines = f.readlines()

    resources = set()
    listening = False
    for line in [line.strip() for line in lines]:
        if line.startswith('DOMAIN_DEFINITIONS'):
            listening = True
            continue

        if not listening:
            continue

        if line.startswith('}'):
            break

        if ':' not in line:
            continue

        resource = line.split(':')[0].strip().replace('"', '').replace("'", '')
        if resource.startswith('_'):
            continue

        resources.add(resource)

    hypermea.tool.jump_back_to(starting_folder)
    return sorted(resources)


def _create_resource_domain_file(resource, add_common):
    with open(f'domain/{resource}.py', 'w') as file:
        file.write(f'''"""
Defines the {resource} resource.
"""
''')

        if add_common:
            file.write('from domain._common import COMMON_FIELDS\n\n\n')

        file.write('''SCHEMA = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'unique': True
    },
    'description': {
        'type': 'string'
    }
}

''')

        if add_common:
            file.write('SCHEMA.update(COMMON_FIELDS)\n\n')

        file.write('''DEFINITION = {
    'schema': SCHEMA,
    'datasource': {
        'projection': {'_owner': 0}
    },
    'additional_lookup': {
        'url': r'regex("[\w]+")',
        'field': 'name'
    }
}
''')


def _create_resource_hook_file(singular, plural):
    with open(f'hooks/{plural}.py', 'w') as file:
        file.write(f'''"""
hooks.{plural}
This module defines functions to add link relations to {plural}.
"""
import logging
import json
from flask import request
from hypermea.core.logging import trace
from configuration import SETTINGS
from hypermea.core.utils import get_resource_id, get_id_field, get_my_base_url, clean_href
from hypermea.core.gateway import get_href_from_gateway
import affordances

LOG = logging.getLogger('hooks.{plural}')


@trace
def add_hooks(app):
    """Wire up the hooks for {plural}."""
    app.on_fetched_item_{plural} += _add_links_to_{singular}
    app.on_fetched_resource_{plural} += _add_links_to_{plural}_collection
    app.on_post_POST_{plural} += _post_{plural}


@trace
def _post_{plural}(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_{plural}_collection(j, request.url)
        else:
            _add_links_to_{singular}(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_{plural}_collection({plural}_collection, self_href=None):
    if 'links-only' in request.args:
        del {plural}_collection['_items']

    if '_items' in {plural}_collection:
        for {singular} in {plural}_collection['_items']:
            _add_links_to_{singular}({singular})

    if '_links' not in {plural}_collection:
        {plural}_collection['_links'] = {{
            'self': {{
                'href': self_href
            }}
        }}

    for rel in ['self', 'prev', 'next', 'last']:
        if rel in {plural}_collection['_links']:
            {plural}_collection['_links'][rel]['href'] = clean_href({plural}_collection['_links'][rel]['href'])

    base_url = get_my_base_url()

    id_field = get_id_field('{plural}')
    if id_field.startswith('_'):
        id_field = id_field[1:]

    {plural}_collection['_links']['item'] = {{
        'href': f'{{base_url}}/{plural}/{{{{{{id_field}}}}}}',
        'title': '{singular}',
        'templated': True
    }}
    
    affordances.rfc6861.create_form.add_link({plural}_collection, '{plural}', '/{plural}')


@trace
def _add_links_to_{singular}({singular}):
    base_url = get_my_base_url()
    {singular}_id = get_resource_id({singular}, '{plural}')

    _add_remote_children_links({singular})
    _add_remote_parent_links({singular})

    {singular}['_links']['self'] = {{
        'href': f"{{base_url}}/{plural}/{{{singular}_id}}",
        'title': '{singular}'
    }}
    affordances.rfc6861.edit_form.add_link({singular}, '{plural}')



@trace
def _add_remote_children_links({singular}):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    {singular}_id = get_resource_id({singular}, '{plural}')

    # == do not edit this method above this line ==


@trace
def _add_remote_parent_links({singular}):
    if not SETTINGS['HY_GATEWAY_URL']:
        return
    {singular}_id = get_resource_id({singular}, '{plural}')

    # == do not edit this method above this line ==
''')


def _insert_domain_definition(resource):
    DomainDefinitionInserter(resource).transform('domain/__init__.py')


def _insert_hooks(resource):
    HooksInserter(resource).transform('hooks/__init__.py',)


def _remove_domain_definition(resource):
    DomainResourceRemover(resource).transform('domain/__init__.py')


def _remove_hooks(resource):
    HooksRemover(resource).transform('hooks/__init__.py')


def _delete_resource_files(resource):
    domain_filename = f'domain/{resource}.py'
    hooks_filename = f'hooks/{resource}.py'

    hypermea.tool.remove_file_if_exists(domain_filename)
    hypermea.tool.remove_file_if_exists(hooks_filename)

    domain_file_exists = os.path.exists(domain_filename)
    hooks_file_exists = os.path.exists(hooks_filename)

    if domain_file_exists or hooks_file_exists:
        which = ''
        which += domain_filename if domain_file_exists else ''
        if hooks_file_exists:
            which += ', ' if which else ''
            which += hooks_filename
        hypermea.tool.escape(f'Could not delete resource files: {which}', 704)


def _remove_references_from_children(resource):
    files = glob.glob('domain/*.py')
    for filename in [file for file in files if not (file.startswith('domain/_') or file.startswith('domain\\_'))]:
        ParentReferenceRemover(resource).transform(filename)


def _remove_child_links(resource):
    files = glob.glob('hooks/*.py')
    for filename in [file for file in files if not (file.startswith('hooks/_') or file.startswith('hooks\\_'))]:
        ChildLinksRemover(resource).transform(filename)
