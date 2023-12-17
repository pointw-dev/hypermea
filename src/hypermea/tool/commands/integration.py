import os
import click
from .command_help_order import CommandHelpOrder
import hypermea.tool


def _get_integrations():
    integrations_folder = os.path.join(os.path.dirname(hypermea.tool.__file__), 'skel/integration')
    integrations = [name for name in os.listdir(integrations_folder) ]
    return integrations


@click.group(name='integration',
             help='Manage integrations with external services.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


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
    from ._integration import _create
    return _create(integration, name, prefix)


@commands.command(name='list',
                  short_help='Lists the integrations that have been added.',
                  help_priority=2)
def list_integrations():
    from ._integration import _list_integrations
    return _list_integrations()
