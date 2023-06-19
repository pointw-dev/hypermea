import click
from .command_help_order import CommandHelpOrder


@click.group(name='setting',
             help='Manage the configuration/settings of the service and its addins.',
             cls=CommandHelpOrder)
def commands():
    pass


@commands.command(name='create',
                  help='(not yet implemented)',
                  help_priority=1)
def create():
    click.echo(f'create')


@commands.command(name='list',
                  help='(not yet implemented)',
                  help_priority=2)
def list_settings():
    click.echo('list')


@commands.command(name='remove',
                  help='(not yet implemented)',
                  help_priority=3)
def remove():
    click.echo('remove')
