import click
from .command_help_order import CommandHelpOrder


@click.group(name='link',
             help='Manage parent/child links amongst resources.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


@commands.command(name='create',
                  short_help='Create a parent/child link between two resources.  If one of the resources is in the '
                       'domain of a different HypermeaService, add "external:" in front of the name of that resource.',
                  help_priority=1)
@click.argument('parent', metavar='<parent|external:parent>')
@click.argument('child', metavar='<child|external:child>')
def create(parent, child):
    from ._link import _create
    return _create(parent, child)


# TODO: refactor/SLAP
@commands.command(name='list',
                  short_help='List the relationships amongst the resources.',
                  help_priority=2)
@click.option('output', '--format', '-f',
              type=click.Choice(['english', 'commands', 'raw', 'json', 'python_dict', 'plant_uml']),
              default='english',
              help='Choose the output format of the relationships list')
def list_rels(output):
    from ._link import _list_rels
    return _list_rels(output)


@commands.command(name='remove',
                  short_help='Remove a link',
                  help_priority=3)
@click.argument('parent', metavar='<parent|external:parent>')
@click.argument('child', metavar='<child|external:child>')
def remove(parent, child):
    from ._link import _remove
    return _remove(parent, child)
