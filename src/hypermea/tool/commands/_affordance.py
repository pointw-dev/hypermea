import glob
import os
import re

import click

import hypermea.tool
from hypermea.tool.code_gen import AffordanceLinkInserter, AffordanceRouteRemover, AffordanceRemover, \
    AffordanceImportRemover, AffordanceRouteInserter
from hypermea.tool.commands.affordance import NA

ROUTE_TEMPLATE = """    @app.route("/{plural}/<{singular}_id>/{affordance_name}", methods=["PUT"])
    def do_{affordance_identifier}_{singular}({singular}_id):
        if app.auth and (not app.auth.authorized(None, "{affordance_name}", "PUT")):
            return make_error_response(unauthorized_message, 401)

        return _do_{affordance_identifier}_{singular}({singular}_id)
"""

HANDLER_TEMPLATE = """def _do_{affordance_identifier}_{singular}({singular}_id):   
    return make_response('affordances.{affordance_fullname} is not yet implemented for {{plural}}', 501)
"""


def _write_affordance_file(affordance, resource_name):
    singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY
    route = ROUTE_TEMPLATE.format(
        affordance_name=affordance.name,
        affordance_identifier=affordance.identifier,
        plural=plural,
        singular=singular
    )
    handler = HANDLER_TEMPLATE.format(
        affordance_identifier=affordance.identifier,
        affordance_fullname=affordance.full_name,
        plural=plural,
        singular=singular
    )

    contents = f'''"""
This module defines functions to add affordances.{affordance.full_name}.
"""
import logging
from flask import make_response
from hypermea.core.utils import make_error_response, unauthorized_message, get_resource_id, get_id_field, get_my_base_url

LOG = logging.getLogger("affordances.{affordance.full_name}")


def add_affordance(app):
{'    pass' if resource_name == NA else route}


def add_link(resource, collection_name):
    base_url = get_my_base_url()
    resource_id = get_resource_id(resource, collection_name)

    resource['_links']['{affordance.name}'] = {{
        'href': f'{{base_url}}/{{collection_name}}/{{resource_id}}/{affordance.name}',
        'title': 'PUT to do {affordance.name}'    
    }}

{'' if resource_name == NA else handler }'''

    with open(f'{affordance.identifier}.py', 'w') as file:
        file.write(contents)


def _affordance_is_already_attached(affordance, resource_name):
    if resource_name == NA:
        return False
    affordances = _get_affordances()

    singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY

    return plural in affordances.get(affordance.name, [])


def _resource_exists(resource_name):
    if resource_name == NA:
        return True
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY

    hypermea.tool.jump_back_to(starting_folder)
    return os.path.exists(f'hooks/{plural}.py')


def _append_import_if_needed(filename, import_statement):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            contents = file.read()

        if import_statement in contents:
            return

    with open(filename, 'a') as file:
        file.write(f'{import_statement}\n')


def _get_affordances():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    rtn = {}
    if os.path.exists('affordances'):
        os.chdir('affordances')
        files = glob.glob('**/*.py', recursive=True)
        for filename in files:
            with open(filename, 'r') as f:
                contents = f.read()
            if 'def add_affordance(app):' in contents:
                affordance = filename.replace('\\', '.').replace('/', '.')[:-3]
                attaches = re.findall(r'@app\.route\(\"\/(.*?)\/', contents)
                rtn[affordance] = attaches

    hypermea.tool.jump_back_to(starting_folder)
    return rtn


def _add_affordance_resource(affordance, resource):
    singular, plural = hypermea.tool.get_singular_plural(resource)  # TODO: DRY
    AffordanceLinkInserter(affordance, singular, plural).transform(f'hooks/{plural}.py')


def _detach_affordance(affordance, resource_name):
    singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY
    click.echo(f'Detaching affordances.{affordance.full_name} from {resource_name}')
    AffordanceRouteRemover(affordance, singular).transform(affordance.filename)
    AffordanceRemover(affordance, singular).transform(f'hooks/__init__.py')
    AffordanceRemover(affordance, singular).transform(f'hooks/{plural}.py')


def _detach_all_resources(affordance):
    affordances = _get_affordances()
    if affordance.full_identifier in affordances:
        for resource_name in affordances[affordance.full_identifier]:
            _detach_affordance(affordance, resource_name)


def _remove_affordance(affordance):
    click.echo(f'Removing affordances.{affordance.full_name}')
    os.remove(f'affordances/{affordance.folder + "/" if affordance.folder else ""}{affordance.name}.py')
    for filename in [file for file in glob.glob('hooks/*.py') if
                     not (file.startswith('hooks/_') or file.startswith('hooks\\_'))]:
        resource_name = filename[6:-3]
        singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY
        AffordanceRemover(affordance, singular).transform(filename)
    AffordanceImportRemover(affordance.identifier).transform(
        f'affordances/{affordance.folder + "/" if affordance.folder else ""}__init__.py')


class Affordance:
    def __init__(self, name):
        self.folder = ''
        if '.' in name:
            # ASSERT: folder was not specified (else warn? abort?)
            # ASSERT: only one dot in affordance_name
            # ASSERT: everything else I'm not thinking about right now
            self.folder, self.name = name.split('.')
        else:
            self.name = name

    @property
    def identifier(self):
        rtn = self.name.replace('-', '_')
        rtn = ''.join(filter(
            lambda c: str.isidentifier(c) or str.isdecimal(c), rtn))
        return rtn

    @property
    def full_name(self):
        return f'{self.folder + "." if self.folder else ""}{self.name}'

    @property
    def full_identifier(self):
        return f'{self.folder + "." if self.folder else ""}{self.identifier}'

    @property
    def filename(self):
        return f'affordances/{self.folder + "/" if self.folder else ""}{self.identifier}.py'


def _create(affordance_name, resource_name):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    # TODO: SLAP!
    # TODO: Use LinkManager pattern
    affordance = Affordance(affordance_name)
    creating = f'Creating {affordance.full_name}'
    if resource_name != NA:
        creating += f' and attaching to {resource_name}'

    if os.path.exists(affordance.filename):
        return hypermea.tool.escape(f'affordances.{affordance.full_name} already exists', 1001)

    if not _resource_exists(resource_name):
        return hypermea.tool.escape(f'cannot attach {affordance.full_name}: {resource_name} does not exist', 1003)

    click.echo(creating)

    if not os.path.exists('affordances'):
        os.mkdir('affordances')
    os.chdir('affordances')

    if affordance.folder:
        if not os.path.exists(affordance.folder):
            os.mkdir(affordance.folder)
        os.chdir(affordance.folder)

    _write_affordance_file(affordance, resource_name)

    _append_import_if_needed('__init__.py', f'from . import {affordance.identifier}')
    if affordance.folder:
        os.chdir('..')
        _append_import_if_needed('__init__.py', f'from . import {affordance.folder}')
    os.chdir('..')

    AffordanceRouteInserter(affordance).transform(f'hooks/__init__.py')
    if resource_name != NA:
        _add_affordance_resource(affordance, resource_name)
    hypermea.tool.jump_back_to(starting_folder)


def _list_affordances():
    affordances = _get_affordances()
    for affordance in affordances:
        click.echo(affordance)
        if affordances[affordance]:
            click.echo('- attached to')
            for resource in affordances[affordance]:
                click.echo(f'  - {resource}')


def _remove(affordance_name, resource_name):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    affordance = Affordance(affordance_name)
    if not os.path.exists(affordance.filename):
        hypermea.tool.jump_back_to(starting_folder)
        return hypermea.tool.escape(f'affordances.{affordance.full_name} does not exist', 1002)

    if resource_name == NA:
        _detach_all_resources(affordance)
        _remove_affordance(affordance)
    else:
        _detach_affordance(affordance, resource_name)
    hypermea.tool.jump_back_to(starting_folder)


def _attach(affordance_name, resource_name):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    # TODO: SLAP!
    # TODO: Use LinkManager pattern
    affordance = Affordance(affordance_name)
    attaching = f'Attaching {affordance.name} to {resource_name}'
    if not os.path.exists(affordance.filename):
        hypermea.tool.jump_back_to(starting_folder)
        return hypermea.tool.escape(f'affordances.{affordance.full_name} does not exist', 1002)

    if not _resource_exists(resource_name):
        return hypermea.tool.escape(f'cannot attach {affordance.full_name}: {resource_name} does not exist', 1003)

    if _affordance_is_already_attached(affordance, resource_name):
        return hypermea.tool.escape(f'{affordance.full_name} is already attached to {resource_name}', 1004)

    click.echo(attaching)

    singular, plural = hypermea.tool.get_singular_plural(resource_name)  # TODO: DRY
    route = ROUTE_TEMPLATE.format(
        affordance_name=affordance.name,
        affordance_identifier=affordance.identifier,
        plural=plural,
        singular=singular
    )
    handler = HANDLER_TEMPLATE.format(
        affordance_identifier=affordance.identifier,
        affordance_fullname=affordance.full_name,
        plural=plural,
        singular=singular
    )

    with open(affordance.filename, 'r') as f:
        lines = f.readlines()

    with open(affordance.filename, 'w') as f:
        for line in lines:
            if line == '    pass\n':
                continue
            f.write(line)
            if line.startswith('def add_affordance('):
                f.write(route)
                f.write('\n')
        f.write('\n')
        f.write(handler)

    _add_affordance_resource(affordance, resource_name)
    hypermea.tool.jump_back_to(starting_folder)
