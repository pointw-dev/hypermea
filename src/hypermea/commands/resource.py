import click
from .command_help_order import CommandHelpOrder


@click.group(name='resource',
             help='Manage the resources that make up the domain of the service.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


@commands.command(name='create',
                  short_help='Create a new resource and add it to the domain.',
                  help_priority=1)
@click.argument('resource_name', metavar='<name>')
@click.option('--no_common', '-c', is_flag=True, help='Do not add common fields to this resource')
def create(resource_name, no_common):
    """Create a new resource and add it to the domain.

    <name> of the resource to create.  Enter either singular or plural and hypermea will choose the other. Or enter both singular and plural separted by a comma.

           e.g. if you enter "cactus" hypermea mistakenly believes that is the plural of "cactu" so enter "cactus,cactuses" or "cactus,cacti" to override hypermea's decision"""
    from ._resource import _create
    return _create(resource_name, no_common)


@commands.command(name='list',
                  short_help='List the resources in the domain.',
                  help_priority=2)
def list_resources():
    from ._resource import _list_resources
    return _list_resources()


@commands.command(name='remove',
                  short_help='Remove a resource',
                  help_priority=3)
@click.argument('resource_name', metavar='<name>')
def remove(resource_name):
    from ._resource import _remove
    return _remove(resource_name)


@commands.command(name='check',
                  short_help='See what the singular/plural of the resource will be.',
                  help_priority=4)
@click.argument('resource_name', metavar='<name>')
def check(resource_name):
    """See what the singular or plural of a resource name will be

    <name> of the resource to check.  Enter singular or plural to see what hypermea will choose for the other."""
    from ._resource import _check
    return _check(resource_name)
