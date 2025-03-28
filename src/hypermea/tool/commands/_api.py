import importlib
import json
import os
import re
import keyword
from shutil import copyfile, copytree, move

import click

import hypermea.tool
from hypermea.tool import addins


def _sanitize_for_python_module_name(name: str) -> str:
    name = name.lower()
    name = re.sub(r'\W+', '_', name)
    name = name.strip('_')
    if name and name[0].isdigit():
        name = f'_{name}'
    if keyword.iskeyword(name):
        name = f'{name}_mod'
    if not name:
        name = 'api'

    return name


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

    if not _is_folder_ready(current_dir):
        hypermea.tool.escape('Canceling api creation', 3)

    os.chdir(current_dir) ####################????????????????????????????????????????????????????????????????????????
    click.echo(f'Creating {project_name} api')
    skel = os.path.join(os.path.dirname(hypermea.tool.__file__), 'skel')

    _create_hypermea_config_file(project_name)
    _copy_documentation(skel)
    _create_idea_folder(project_name, skel)

    os.mkdir('src')
    os.chdir('src')

    _create_scripts_folder(skel)
    _create_features_folder(project_name, skel)
    _create_service_folder(project_name, skel)
    _remove_pycache_folders(project_name)

    os.chdir('..')
    hypermea.tool.replace_project_name(project_name, '.')


def _remove_pycache_folders(project_name):
    # TODO: can the following remove_tree calls be obviated if skel is packaged differently?
    hypermea.tool.remove_folder_if_exists(project_name, '__pycache__', recursive=True)
    hypermea.tool.remove_folder_if_exists('scripts', '__pycache__', recursive=True)


def _create_service_folder(project_name, skel):
    folder_name = 'service'
    _copy_api_skel(project_name, folder_name, skel)
    _rename_test_templates(project_name, folder_name)
    _rename_api_settings(project_name, folder_name)


def _rename_api_settings(project_name, folder_name):
    module_name = _sanitize_for_python_module_name(project_name)
    config_init = os.path.join(folder_name, 'configuration/__init__.py')
    with open(config_init, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('api_settings', f'{module_name}_settings')
    with open(config_init, 'w', encoding='utf-8') as f:
        f.write(content)
    os.rename(os.path.join(folder_name, 'configuration/api_settings.py'),
              os.path.join(folder_name, f'configuration/{module_name}_settings.py'))


def _rename_test_templates(project_name, folder_name):
    directory = os.path.realpath(os.path.join(folder_name, f'__tests__'))
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.find('.py.template') > 0:
                file_path = os.path.join(subdir, filename)
                new_file_path = file_path.replace('.py.template', '.py')
                os.rename(file_path, new_file_path)


def _copy_api_skel(project_name, folder_name, skel):
    os.mkdir(folder_name)
    api_folder = os.path.join(skel, 'api')
    copytree(api_folder, folder_name, dirs_exist_ok=True)
    move(os.path.join(folder_name, f'__tests__/project_name'), os.path.join(folder_name, f'__tests__/{project_name}'))


def _create_features_folder(project_name, skel):
    folder_name = 'features'
    os.mkdir(folder_name)
    os.mkdir(f'{folder_name}/{project_name}')
    features_folder = os.path.join(skel, folder_name)
    copytree(features_folder, folder_name, dirs_exist_ok=True)


def _create_scripts_folder(skel):
    folder_name = 'scripts'
    os.mkdir(folder_name)
    scripts_folder = os.path.join(skel, folder_name)
    copytree(scripts_folder, folder_name, dirs_exist_ok=True)


def _copy_documentation(skel):
    readme_filename = os.path.join(skel, 'doc/README.md')
    copyfile(readme_filename, './README.md')
    # TODO: write good docs and put them here...
    # os.mkdir('doc')
    # readme_filename = os.path.join(skel, 'doc/Setup-Dev-Environment.md')
    # copyfile(readme_filename, './doc/Setup-Dev-Environment.md')
    # hypermea.tool.replace_project_name(project_name, 'doc')

def _create_idea_folder(project_name, skel):
    idea_target_folder = '.idea'
    os.mkdir(idea_target_folder)
    copytree(os.path.join(skel, 'idea'), idea_target_folder, dirs_exist_ok=True)
    move(os.path.join(idea_target_folder, 'project_name.iml'), os.path.join(idea_target_folder, f'{project_name}.iml'))
    hypermea.tool.replace_project_name(project_name, idea_target_folder)



def _create_hypermea_config_file(project_name):
    settings = {
        'project_name': project_name
    }
    with open('.hypermea', 'w') as f:
        json.dump(settings, f, indent=4)


def _is_folder_ready(current_dir):
    cur_dir_contents = os.listdir(current_dir)
    folder_is_empty = len(cur_dir_contents) == 0
    if len(cur_dir_contents) == 1 and '.python-version' in cur_dir_contents:
        folder_is_empty = True
    if folder_is_empty:
        return True
    else:
        return  click.confirm(
            'This folder is not empty.  Do you still wish to create your API here?',
            show_default=True
        )




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
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service/configuration')
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
