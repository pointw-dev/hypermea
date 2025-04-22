import os
import sys

import hypermea.tool
from hypermea.tool.code_gen import SettingsInserter, AllSettingsInserter



def _create(integration, name, prefix):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    if integration == 'custom' and name is None:
        print('You must supply a name when choosing the "custom" integration.')
        hypermea.tool.jump_back_to(starting_folder)
        sys.exit(902)

    if name is None:
        name = integration

    # TODO: ensure name is folder name friendly

    if os.path.exists(f'integration/{name}'):
        print(f'There already is an integration named "{name}".')
        hypermea.tool.jump_back_to(starting_folder)
        sys.exit(901)

    print(f'creating {name} integration')

    if not os.path.exists('integration'):
        os.makedirs('integration')
    if not os.path.exists(f'integration/{integration}'):
        os.makedirs(f'integration/{integration}')

    replace = {
        'integration': name.title(),
        'prefix': prefix.upper() if prefix else name.upper()
    }
    hypermea.tool.copy_skel(settings['project_name'], f'integration/{integration}',
                                  target_folder=f'integration/{integration}',
                                  replace=replace)

    if integration == 'custom':
        # rename the folder from integration to name
        os.rename(f'integration/{integration}', f'integration/{name.lower()}')

    with open(f'./integration/__init__.py', 'a') as f:
        f.write(f'from . import {name.lower()}\n')

    SettingsInserter('integration', f'{name.title()}Settings').transform('./settings/__init__.py')
    AllSettingsInserter('integration', f'{name.title()}Settings').transform('./settings/all_settings.py')
    hypermea.tool.run_setup(integration)

    # TODO: ensure outer requirements.txt contains libraries required by the integration
    hypermea.tool.jump_back_to(starting_folder)


def _list_integrations():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    if not os.path.exists('integration'):
        print('No integrations have been added')
        hypermea.tool.jump_back_to(starting_folder)
        sys.exit(0)

    integrations =  [name for name in os.listdir('./integration') ]
    for integration in integrations:
        if integration.startswith('_'):
            continue
        print(f'- {integration}')

    hypermea.tool.jump_back_to(starting_folder)
