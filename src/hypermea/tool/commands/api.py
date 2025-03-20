import functools
import click
from .command_help_order import CommandHelpOrder
from .optional_flags import OptionalFlags


@click.group(cls=CommandHelpOrder, name='api', help='Create and manage the API service itself.')
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


def addin_params(func):
    @click.option('--add-git', '-g',
                  is_flag=True,
                  help='initialize local git repository (with optional remote)',
                  flag_value='no remote',
                  metavar='[remote]')
    @click.option('--add-docker', '-d',
                  is_flag=True,
                  help='add Dockerfile and supporting files to deploy the API as a container',
                  flag_value='n/a')
    @click.option('--add-auth', '-a',
                  is_flag=True, help='add authorization class and supporting files',
                  flag_value='n/a')
    @click.option('--add-validation', '-v',
                  is_flag=True,
                  help='add custom validation class that you can extend',
                  flag_value='n/a')
    @click.option('--add-websocket', '-w',
                  is_flag=True,
                  help='add web socket and supporting files',
                  flag_value='n/a')
    @click.option('--add-serverless', '-s',
                  is_flag=True,
                  help='add serverless framework and supporting files',
                  flag_value='n/a')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@commands.command(name='create',
                  short_help="<name> or '.' to use the current folder's name",
                  cls=OptionalFlags,
                  help_priority=1)
@click.argument('project_name', metavar='<name>')
@addin_params
def create(**kwargs):
    """<name> or "." to use the current folder's name"""
    from ._api import _create_api, _add_addins
    _create_api(kwargs['project_name'])
    del kwargs['project_name']
    _add_addins(kwargs)


@commands.command(name='addin',
                  short_help='Add an addin to an already created API',
                  cls=OptionalFlags,
                  help_priority=2)
@addin_params
def addin(**kwargs):
    """Add an addin to an already created API"""
    from ._api import _add_addins
    return _add_addins(kwargs)


@commands.command(name='version',
                  short_help='View or set the version number of the API',
                  help_priority=3)
@click.argument('set_version', metavar='[version]', default=None, required=False)
def version(set_version):
    """View or set the version number of the API"""
    from ._api import _show_or_set_version
    return _show_or_set_version(set_version)
