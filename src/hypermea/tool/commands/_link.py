import json
import sys

import click

import hypermea.tool
from hypermea.tool.commands.link_manager import LinkManager, LinkManagerException


def _create(parent, child, as_parent_ref):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child, as_parent_ref).add()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)
    finally:
        hypermea.tool.jump_back_to(starting_folder)


def _list_rels(output):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/domain')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    rels = LinkManager.get_relations()

    globals()[f'_print_{output}'](rels)

    # if output == 'english':
    #     _print_english(rels)
    # elif output == 'json':
    #     _print_json(rels)
    # elif output == 'python_dict':
    #     _print_python_dict(rels)
    # elif output == 'plant_uml':  # TODO: wonky/needs help
    #     _print_plant_uml(rels)
    hypermea.tool.jump_back_to(starting_folder)


def _print_plant_uml(rels):
    print('@startuml')
    _print_plant_uml_start()
    _print_plant_uml_classes(rels)
    print()
    _print_plant_uml_relations(rels)
    print('@enduml')


def _print_plant_uml_relations(rels):
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


def _print_plant_uml_classes(rels):
    for rel in rels:
        if ':' not in rel:
            print(f'class {rel} <<resource>>')
        for item in rels[rel]:
            for member in rels[rel][item]:
                if member.startswith(LinkManager.REMOTE_PREFIX):
                    target = member[len(LinkManager.REMOTE_PREFIX):]
                    print(f'class {target} <<remote>>')


def _print_plant_uml_start():
    print('hide <<resource>> circle')
    print('hide <<remote>> circle')
    print('hide members ')
    print()
    print('skinparam class {')
    print('    BackgroundColor<<remote>> LightBlue')
    print('}')
    print()


def _print_python_dict(rels):
    print(rels)


def _print_json(rels):
    print(json.dumps(rels, indent=4, default=list))


def _print_english(rels):
    for rel in rels:
        print(rel)
        for item in rels[rel].get('parents', []):
            article = 'an' if item[0].lower() in 'aeiou' else 'a'
            print(f'- belong to {article} {item}')
        for item in rels[rel].get('children', []):
            print(f'- have {item}')


def _remove(parent, child):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child).remove()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)
    finally:
        hypermea.tool.jump_back_to(starting_folder)
