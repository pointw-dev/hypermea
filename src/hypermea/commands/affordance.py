import click
from .command_help_order import CommandHelpOrder
from .optional_flags import OptionalFlags

NA = 'n/a'


@click.group(name='affordance',
             help='Manage link rels that operate on the state of resources.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
    pass


@commands.command(name='create',
                  short_help='Creates an affordance, adds a route, and _links to a resource',
                  cls=OptionalFlags,
                  help_priority=1)
@click.argument('affordance_name', metavar='<name>')
@click.argument('resource_name', metavar='[resource]', default=NA)
def create(affordance_name, resource_name):
    """
    Creates an affordance, adds a route from a resource, and wires the affordance's
    path into the _links of a given resource.
    """
    from ._affordance import _create
    return _create(affordance_name, resource_name)


@commands.command(name='list',
                  short_help='List the affordances in the API',
                  help_priority=2)
def list_affordances():
    """
    Lists affordances previously created
    """
    from ._affordance import _list_affordances
    return _list_affordances()


@commands.command(name='remove',
                  short_help='Removes an affordance, or detaches it from a resource',
                  help_priority=3)
@click.argument('affordance_name', metavar='<name>')
@click.argument('resource_name', metavar='[resource]', default=NA)
def remove(affordance_name, resource_name):
    from ._affordance import _remove
    return _remove(affordance_name, resource_name)


@commands.command(name='attach',
                  short_help='Attach an existing affordance to a resource',
                  cls=OptionalFlags,
                  help_priority=4)
@click.argument('affordance_name', metavar='<name>')
@click.argument('resource_name', metavar='<resource>')
def attach(affordance_name, resource_name):
    """
    Creates a route to previously created affordance for a resource, and wires the affordance's
    route into the _links of the resource.
    """
    from ._affordance import _attach
    return _attach(affordance_name, resource_name)

