import json
import sys
import click
from .command_help_order import CommandHelpOrder
from .link_manager import LinkManager, LinkManagerException
import hypermea


@click.group(name='link',
             help='Manage parent/child links amongst resources.',
             cls=CommandHelpOrder)
def commands():
    pass


@commands.command(name='create',
                  short_help='Create a parent/child link between two resources.  If one of the resources is in the '
                       'domain of a different HypermeaService, add "remote:" in front of the name of that resource.',
                  help_priority=1)
@click.argument('parent', metavar='<parent|remote:parent>')
@click.argument('child', metavar='<child|remote:child>')
@click.option('--as_parent_ref', '-p',
              is_flag=True,
              help='Change name of related ref to "parent" (instead of the name of the parent).')
def create(parent, child, as_parent_ref):
    try:
        starting_folder, settings = hypermea.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child, as_parent_ref).add()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)


# TODO: refactor/SLAP
@commands.command(name='list',
                  short_help='List the relationships amongst the resources.',
                  help_priority=2)
@click.option('output', '--format', '-f',
              type=click.Choice(['english', 'json', 'python_dict', 'plant_uml']),
              default='english',
              help='Choose the output format of the relationships list')
def list_rels(output):
    try:
        starting_folder, settings = hypermea.jump_to_folder('src/{project_name}/domain')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    rels = LinkManager.get_relations()

    if output == 'english':
        for rel in rels:
            print(rel)
            for item in rels[rel].get('parents', []):
                print(f'- belong to a {item}')
            for item in rels[rel].get('children', []):
                print(f'- have {item}')
    elif output == 'json':
        print(json.dumps(rels, indent=4, default=list))
    elif output == 'python_dict':
        print(rels)
    elif output == 'plant_uml':  # TODO: wonky/needs help
        print('@startuml')
        print('hide <<resource>> circle')
        print('hide <<remote>> circle')
        print('hide members ')
        print()
        print('skinparam class {')
        print('    BackgroundColor<<remote>> LightBlue')
        print('}')
        print()
        for rel in rels:
            if ':' not in rel:
                print(f'class {rel} <<resource>>')
            for item in rels[rel]:
                for member in rels[rel][item]:
                    if member.startswith(LinkManager.REMOTE_PREFIX):
                        target = member[len(LinkManager.REMOTE_PREFIX):]
                        print(f'class {target} <<remote>>')
        print()
        for rel in rels:
            for item in rels[rel].get('children', []):
                if item.startswith(LinkManager.REMOTE_PREFIX):
                    item = item[len(LinkManager.REMOTE_PREFIX):]
                if ':' not in rel:
                    print(f'{rel} ||--o{{ {item}')
            for item in rels[rel].get('parents', []):
                if item.startswith(LinkManager.REMOTE_PREFIX):
                    item = item[len(LinkManager.REMOTE_PREFIX):]
                    if ':' not in item:
                        print(f'{item} ||--o{{ {rel}')
        print('@enduml')


@commands.command(name='remove',
                  short_help='Remove a link',
                  help_priority=3)
@click.argument('parent', metavar='<parent|remote:parent>')
@click.argument('child', metavar='<child|remote:child>')
def remove(parent, child):
    try:
        hypermea.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child).remove()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)
