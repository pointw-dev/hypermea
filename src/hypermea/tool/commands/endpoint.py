import click
from .command_help_order import CommandHelpOrder


@click.group(name='endpoint',
             help='Manage non-resource endpoints.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


@commands.command(name='create',
                  short_help='(not yet implemented)',
                  help_priority=1)
def create():
    from ._endpoint import _create
    return _create()


@commands.command(name='list',
                  short_help='(not yet implemented)',
                  help_priority=2)
def list_endpoints():
    from ._endpoint import _list_endpoints
    return _list_endpoints()


@commands.command(name='remove',
                  short_help='(not yet implemented)',
                  help_priority=3)
def remove():
    from ._endpoint import _remove
    return _remove()
