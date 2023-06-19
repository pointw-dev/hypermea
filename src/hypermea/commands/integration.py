import os
import sys
import click
from .command_help_order import CommandHelpOrder
import hypermea


@click.group(name='integration',
             help='Manage integrations with external services.',
             cls=CommandHelpOrder)
def commands():
    pass


def _get_integrations():
    integrations_folder = os.path.join(os.path.dirname(hypermea.__file__), 'skel/integration')
    integrations = [name for name in os.listdir(integrations_folder) ]
    return integrations


@commands.command(name='create',
                  short_help=f'Create an external integration to the service.',
                  help_priority=1)
@click.argument('integration', type=click.Choice(_get_integrations(), case_sensitive=False), metavar='<integration>')
@click.option('--name', '-n',
              help='Set or change the name of the integration.  If you do not supply a name, the name of '
                   'the integration will be used (e.g. s3).  If you choose "empty" you must supply a name.',
              metavar='[name]')
@click.option('--prefix', '-p',
              help='Set the prefix used in settings this integration may require.',
              metavar='[prefix]')
def create(integration, name, prefix):
    """
    Create an external integration to the service.
    
    Integrations are used to keep separate the code you use to access other services, utilities, etc.
    
    Type 'hypermea integration create' by itself to see a list of integrations available.
    """
    try:
        settings = hypermea.jump_to_api_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    if integration == 'empty' and name is None:
        print('You must supply a name when choosing the "empty" integration.')
        sys.exit(902)

    if name is None:
        name = integration

    # TODO: ensure name is folder name friendly
    
    if os.path.exists(f'integration/{name}'):
        print(f'There already is an integration named "{name}".')
        sys.exit(901)

    print(f'creating {name} integration')

    if not os.path.exists('integration'):
        os.makedirs('integration')
    if not os.path.exists(f'integration/{name}'):
        os.makedirs(f'integration/{name}')

    replace = {
        'integration': name,
        'prefix': prefix.upper() if prefix else name.upper()
    }
    hypermea.copy_skel(settings['project_name'], f'integration/{integration}',
                        target_folder=f'integration/{name}',
                        replace=replace)
    with open(f'./integration/__init__.py', 'a') as f:
        f.write(f'from . import {name}\n')
    # TODO: handle settings/prefix
    # TODO: ensure outer requirements.txt contains libraries required by the integration


@commands.command(name='list',
                  short_help='Lists the integrations that have been added.',
                  help_priority=2)
def list_integrations():
    try:
        settings = hypermea.jump_to_api_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    if not os.path.exists('integration'):
        print('No integrations have been added')
        sys.exit(0)
    
    integrations =  [name for name in os.listdir('./integration') ]
    for integration in integrations:
        if integration.startswith('_'):
            continue
        print(f'- {integration}')
