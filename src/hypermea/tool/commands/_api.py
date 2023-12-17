import importlib
import json
import os
import re
from distutils.dir_util import copy_tree
from shutil import copyfile

import click

import hypermea.tool
from hypermea.tool import addins


def _sanitize_for_mongo_db_name(name: str) -> str:
    if not name:
        raise ValueError("Name cannot be empty")

    # Replace any of the invalid Windows characters with hyphens
    invalid_chars = r'[\/."$*<>:|?]|[\s]+'
    sanitized = re.sub(invalid_chars, '-', name)

    # Eliminate any instances of double hyphens
    sanitized = re.sub(r'-+', '-', sanitized)

    # Ensure the database name starts with a letter or underscore
    if not sanitized[0].isalpha() and sanitized[0] != "_":
        sanitized = "_" + sanitized

    return sanitized


def _api_already_exist():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder()
        hypermea.tool.jump_back_to(starting_folder)
        return True
    except RuntimeError:
        return False


def _create_api(project_name):
    current_dir = os.getcwd()
    if project_name == '.':
        project_name = os.path.basename(os.getcwd())
    if _api_already_exist():
        return hypermea.tool.escape('Please run in a folder that does not already contain an hypermea service', 2)

    project_name = _sanitize_for_mongo_db_name(project_name)

    if len(os.listdir(current_dir)) > 0 and not click.confirm(
            'This folder is not empty.  Do you still wish to create your API here?',
            show_default=True
    ):
        return hypermea.tool.escape('Canceling api creation', 3)

    os.chdir(current_dir)
    click.echo(f'Creating {project_name} api')
    settings = {
        'project_name': project_name
    }
    with open('.hypermea', 'w') as f:
        json.dump(settings, f, indent=4)

    skel = os.path.join(os.path.dirname(hypermea.tool.__file__), 'skel')
    readme_filename = os.path.join(skel, 'doc/README.md')
    copyfile(readme_filename, './README.md')
    os.mkdir('doc')
    readme_filename = os.path.join(skel, 'doc/Setup-Dev-Environment.md')
    copyfile(readme_filename, './doc/Setup-Dev-Environment.md')

    os.mkdir('src')
    os.chdir('src')
    os.mkdir('scripts')
    scripts_folder = os.path.join(skel, 'scripts')
    copy_tree(scripts_folder, 'scripts')

    api_folder = os.path.join(skel, 'api')

    os.mkdir(project_name)
    copy_tree(api_folder, project_name)

    # TODO: can the following remove_tree calls be obviated if skel is packaged differently?
    hypermea.tool.remove_folder_if_exists(os.path.join('scripts', '__pycache__'))
    hypermea.tool.remove_folder_if_exists(os.path.join(project_name, '__pycache__'))
    hypermea.tool.remove_folder_if_exists(os.path.join(project_name, 'configuration', '__pycache__'))
    hypermea.tool.remove_folder_if_exists(os.path.join(project_name, 'domain', '__pycache__'))
    hypermea.tool.remove_folder_if_exists(os.path.join(project_name, 'hooks', '__pycache__'))

    os.chdir('..')
    hypermea.tool.replace_project_name(project_name, '.')


def _add_addins(which_addins, silent=False):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder()
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1, silent)

    for keyword in [kw for kw in which_addins.keys() if which_addins[kw]]:
        addin_name = keyword[4:]  # remove "add-"
        settings_addins = settings.get('addins', {})
        if addin_name in settings_addins:
            if not silent: print(f'{addin_name} is already added.')
            hypermea.tool.jump_back_to(starting_folder)
            return

        if addin_name == 'git':
            settings_addins[addin_name] = {}
            settings = hypermea.tool.add_to_settings('addins', settings_addins)
            continue

        addin_module = importlib.import_module(f'hypermea.tool.addins.{addin_name}')
        add = getattr(addin_module, 'add')
        error_level = 1
        if which_addins[keyword] == 'n/a':
            error_level = add(silent)
        else:
            error_level = add(which_addins[keyword], silent)

        added = error_level == 0
        if added:
            settings_addins[addin_name] = {}
            settings = hypermea.tool.add_to_settings('addins', settings_addins)

    if which_addins.get('add_git', False):
        hypermea.tool.addins.git.add(which_addins['add_git'], silent)

    hypermea.tool.jump_back_to(starting_folder)


def _show_or_set_version(new_version):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}/configuration')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    filename = '__init__.py'
    with open(filename, 'r') as f:
        lines = f.readlines()

    modified = ''
    starts_with = 'VERSION = '

    for line in lines:
        if line.startswith(starts_with):
            print(line.rstrip().lstrip())
            line = f"{starts_with}'{new_version}'\n"

        modified += line

    if new_version:
        print(f'- set to: {new_version}\n')
        with open(filename, 'w') as f:
            f.write(modified)
    else:
        print('- unchanged\n')

    hypermea.tool.jump_back_to(starting_folder)
