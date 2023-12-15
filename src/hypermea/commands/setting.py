import click
from .command_help_order import CommandHelpOrder


@click.group(name='setting',
             help='Manage the configuration/settings of the service and its addins.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


@commands.command(name='create',
                  help='(not yet implemented)',
                  help_priority=1)
def create():
    from ._setting import _create
    return _create()


@commands.command(name='list',
                  help='(not yet implemented)',
                  help_priority=2)
def list_settings():
    from ._setting import _list_setting
    return _list_setting()


@commands.command(name='remove',
                  help='(not yet implemented)',
                  help_priority=3)
def remove():
    from ._setting import _remove
    return _remove()
