import glob
import os

import click

import hypermea.tool
from hypermea.core.domain import list_domain_resources
from hypermea.core.utils import get_singular_plural
from hypermea.tool.code_gen import DomainDefinitionInserter, HooksInserter, DomainResourceRemover, HooksRemover, \
    ParentReferenceRemover, ChildLinksRemover


def _create(resource_name, no_common):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    singular, plural = get_singular_plural(resource_name)
    if _is_resource_name_is_invalid(singular, plural):
        return hypermea.tool.escape(f'The resource name ({resource_name}) is invalid', 701)

    add_common = not no_common

    print(f'Creating {singular} resource')
    if _resource_already_exists(plural):
        hypermea.tool.escape('This resource already exist', 702)
    else:
        _create_resource_domain_file(singular, plural, add_common)
        # _insert_domain_definition(plural)
        _create_resource_hook_file(singular, plural)
        _insert_hooks(singular)

    hypermea.tool.jump_back_to(starting_folder)


def _list_resources():
    resources_list = _get_resource_list()
    for resource in resources_list:
        print('- ' + resource)


def _remove(resource_name):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    singular, plural = get_singular_plural(resource_name)
    if _is_resource_name_is_invalid(singular, plural):
        return hypermea.tool.escape(f'The resource name ({resource_name}) is invalid', 701)

    if not _resource_already_exists(singular):
        hypermea.tool.escape('This resource does not exist', 703)

    #_remove_domain_definition(plural)
    _remove_hooks(singular)
    _delete_resource_files(singular)
    # _remove_references_from_children(plural)
    # _remove_child_links(plural)
    hypermea.tool.jump_back_to(starting_folder)


def _check(resource_name):
    singular, plural = get_singular_plural(resource_name)
    click.echo(f'You entered {resource_name}')
    click.echo(f'- singular: {singular}')
    click.echo(f'- plural:   {plural}')

    click.echo(f'A resource named {singular} ' +
               ('already exists' if _resource_already_exists(plural) else 'does not exist'))


def _resource_already_exists(resource_name):
    resources_list = _get_resource_list()
    return resource_name in resources_list


def _is_resource_name_is_invalid(singular, plural):
    # TODO: check validity of names
    return False


def _get_resource_list():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    resources = list_domain_resources()

    hypermea.tool.jump_back_to(starting_folder)
    return sorted(resources)


def _create_resource_domain_file(singular, plural, add_common):
    with open(f'domain/{singular}.py', 'w') as file:
        file.write(f'''"""
Defines the "{singular}" resource, and its "{plural}" resource collection.
"""
from typing import Optional
from pydantic import BaseModel, Field
from hypermea.core.domain import ResourceModel

class {singular.title()}(ResourceModel):    
    name: str
    description: Optional[str] = None
    
    class Config:
        plural = '{plural}'
''')

    ## common fields (if add_common)
    ##  'projection': {{'_owner': 0}}


def _create_resource_hook_file(singular, plural):
    with open(f'hooks/{singular}.py', 'w') as file:
        file.write(f'''"""
hooks.{singular}
This module defines provides lifecycle hooks for the {singular} resource.
"""
import logging
import json
from flask import request as current_request
from hypermea.core.logging import trace
from hypermea.core.href import get_resource_id, add_etag_header_to_post, get_self_href_from_request
from hypermea.core.gateway import get_href_from_gateway
import settings
import affordances

LOG = logging.getLogger('hooks.{singular}')


@trace
def add_hooks(app):
    """Wire up the hooks for {singular}."""
    app.on_post_POST_{plural} += add_etag_header_to_post
    app.on_post_POST_{plural} += _post_{plural}
    app.on_fetched_item_{plural} += _add_links_to_{singular}
    app.on_fetched_resource_{plural} += _add_links_to_{plural}_collection


@trace
def _post_{plural}(request, payload):
    if payload.status_code == 201:
        j = json.loads(payload.data)
        if '_items' in j:
            _add_links_to_{plural}_collection(j)
        else:
            _add_links_to_{singular}(j)
        payload.data = json.dumps(j)


@trace
def _add_links_to_{plural}_collection({plural}_collection):
    affordances.rfc6861.create_form.add_link({plural}_collection, '{plural}')
    for {singular} in {plural}_collection['_items']:
        _add_links_to_{singular}({singular})


@trace
def _add_links_to_{singular}({singular}):
    _add_external_children_links({singular})
    _add_external_parent_links({singular})
    affordances.rfc6861.edit_form.add_link({singular}, '{plural}')


## The following two methods are here for use by `hy link create`
## Modifying them may make it more difficult to create a link from
## another resource to this one.

@trace
def _add_external_children_links({singular}):
    if not settings.hypermea.gateway_url:
        return
    {singular}_id = get_resource_id({singular}, '{plural}')

    # == do not edit this method above this line ==


@trace
def _add_external_parent_links({singular}):
    if not settings.hypermea.gateway_url:
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
