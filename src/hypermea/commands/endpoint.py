import click

from .command_help_order import CommandHelpOrder


@click.group(name='endpoint',
             help='Manage non-resource endpoints.',
             cls=CommandHelpOrder)
def commands():
    pass


@commands.command(name='create',
                  short_help='(not yet implemented)',
                  help_priority=1)
def create():
    click.echo(f'create')


@commands.command(name='list',
                  short_help='(not yet implemented)',
                  help_priority=2)
def list_endpoints():
    click.echo('list')


@commands.command(name='remove',
                  short_help='(not yet implemented)',
                  help_priority=3)
def remove():
    click.echo('remove')
