import os
import sys

import hypermea
import hypermea.operations


def _create(integration, name, prefix):
    try:
        starting_folder, settings = hypermea.operations.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.operations.escape('This command must be run in a hypermea folder structure', 1)

    if integration == 'empty' and name is None:
        print('You must supply a name when choosing the "empty" integration.')
        hypermea.operations.jump_back_to(starting_folder)
        sys.exit(902)

    if name is None:
        name = integration

    # TODO: ensure name is folder name friendly

    if os.path.exists(f'integration/{name}'):
        print(f'There already is an integration named "{name}".')
        hypermea.operations.jump_back_to(starting_folder)
        sys.exit(901)

    print(f'creating {name} integration')

    if not os.path.exists('integration'):
        os.makedirs('integration')
    if not os.path.exists(f'integration/{name}'):
        os.makedirs(f'integration/{name}')

    replace = {
        'integration': name,
        'prefix': prefix.upper() if prefix else name.upper()
    }
    hypermea.operations.copy_skel(settings['project_name'], f'integration/{integration}',
                                  target_folder=f'integration/{name}',
                                  replace=replace)
    with open(f'./integration/__init__.py', 'a') as f:
        f.write(f'from . import {name}\n')
    # TODO: handle settings/prefix
    # TODO: ensure outer requirements.txt contains libraries required by the integration
    hypermea.operations.jump_back_to(starting_folder)


def _list_integrations():
    try:
        starting_folder, settings = hypermea.operations.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.operations.escape('This command must be run in a hypermea folder structure', 1)

    if not os.path.exists('integration'):
        print('No integrations have been added')
        hypermea.operations.jump_back_to(starting_folder)
        sys.exit(0)

    integrations =  [name for name in os.listdir('./integration') ]
    for integration in integrations:
        if integration.startswith('_'):
            continue
        print(f'- {integration}')

    hypermea.operations.jump_back_to(starting_folder)
