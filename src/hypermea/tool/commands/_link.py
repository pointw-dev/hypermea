import json
import sys
from argparse import ArgumentError

import click

import hypermea.tool
from hypermea.tool.commands.link_manager import LinkManager, LinkManagerException


def _create(parent, child):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child).add()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)
    except ArgumentError as err:
        click.echo(err)
        sys.exit(805)
    finally:
        hypermea.tool.jump_back_to(starting_folder)


def _list_rels(output):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    if output in ['raw', 'commands']:
        registry = LinkManager.get_relation_registry()
        if output == 'raw':
            for rel in registry:
                print(rel)
        if output == 'commands':
            for rel in registry:
                parent = ('external:' if rel.parent.external else '') + str(rel.parent)
                child = ('external:' if rel.child.external else '') + str(rel.child)
                entered = f'hy link create {parent} {child}'
                print(entered)
    else:
        rels = LinkManager.get_relations()
        globals()[f'_print_{output}'](rels)

    hypermea.tool.jump_back_to(starting_folder)

def _print_plant_uml(rels):
    print('@startuml')
    _print_plant_uml_start()
    _print_plant_uml_classes(rels)
    print()
    _print_plant_uml_relations(rels)
    print('@enduml')


def _print_plant_uml_relations(rels):
    relations = set()
    for resource, relationships in rels.items():
        for singular, plural, external in relationships.get('children', []):
            relations.add(f'{resource} ||--o{{ {singular}')
        for singular, plural, external in relationships.get('parents', []):
            relations.add(f'{singular} ||--o{{ {resource}')

    for relation in relations:
        print(relation)


def _print_plant_uml_classes(rels):
    for resource, relationships in rels.items():
        cls = f'class {resource} '
        if relationships['external']:
            cls += '<<external>>'
        else:
            cls += '<<resource>>'
        print(cls)


def _print_plant_uml_start():
    print('hide <<resource>> circle')
    print('hide <<external>> circle')
    print('hide members ')
    print()
    print('skinparam class {')
    print('    BackgroundColor<<external>> LightBlue')
    print('}')
    print()


def _print_python_dict(rels):
    print(rels)


def _print_json(rels):
    print(json.dumps(rels, indent=4, default=list))


def _print_english(rels):
    def apply_article_to_word(word):
        article = 'an' if word[0].lower() in 'aeiou' else 'a'
        return f'{article} {word}'

    for resource, relationships in rels.items():
        label = apply_article_to_word(resource)
        if relationships['external']:
            label += ' (external)'
        print(label)
        for singular, plural, external in relationships.get('parents', []):
            print(f'- belongs to {apply_article_to_word(singular)}{' (external)' if external else ''}')
        for singular, plural, external in relationships.get('children', []):
            print(f'- has {plural}{' (external)' if external else ''}')


def _remove(parent, child):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        LinkManager(parent, child).remove()
    except LinkManagerException as err:
        click.echo(err)
        sys.exit(err.exit_code)
    finally:
        hypermea.tool.jump_back_to(starting_folder)
