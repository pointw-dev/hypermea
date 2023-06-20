import os
import json
import functools
import click
from distutils.dir_util import copy_tree, remove_tree
import importlib
from shutil import copyfile
from .command_help_order import CommandHelpOrder
from .optional_flags import OptionalFlags
from hypermea import addins
import hypermea


@click.group(cls=CommandHelpOrder, name='api', help='Create and manage the API service itself.')
def commands():
    pass


def addin_params(func):
    @click.option('--add-git', '-g',
                  is_flag=True,
                  help='initialize local git repository (with optional remote)',
                  flag_value='no remote',
                  metavar='[remote]')
    @click.option('--add-docker', '-d',
                  is_flag=True,
                  help='add Dockerfile and supporting files to deploy the API as a container',
                  flag_value='n/a')
    @click.option('--add-auth', '-a',
                  is_flag=True, help='add authorization class and supporting files',
                  flag_value='n/a')
    @click.option('--add-validation', '-v',
                  is_flag=True,
                  help='add custom validation class that you can extend',
                  flag_value='n/a')
    @click.option('--add-websocket', '-w',
                  is_flag=True,
                  help='add web socket and supporting files',
                  flag_value='n/a')
    @click.option('--add-serverless', '-s',
                  is_flag=True,
                  help='add serverless framework and supporting files',
                  flag_value='n/a')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@commands.command(name='create',
                  short_help="<name> or '.' to use the current folder's name",
                  cls=OptionalFlags,
                  help_priority=1)
@click.argument('project_name', metavar='<name>')
@addin_params
def create(**kwargs):
    """<name> or "." to use the current folder's name"""
    _create_api(kwargs['project_name'])
    del kwargs['project_name']
    _add_addins(kwargs)


@commands.command(name='addin',
                  short_help='Add an addin to an already created API',
                  cls=OptionalFlags,
                  help_priority=2)
@addin_params
def addin(**kwargs):
    """Add an addin to an already created API"""
    _add_addins(kwargs)


@commands.command(name='version',
                  short_help='View or set the version number of the API, man',
                  cls=OptionalFlags,
                  help_priority=3)
@click.option('new_version', '--set-version', is_flag=True, flag_value='n/a',
              help='set the version number (e.g. --set-version=1.0.0)', metavar='<new-version>')
def version(new_version):
    """View or set the version number of the API"""
    _show_or_set_version(new_version)


def _api_already_exist():
    try:
        starting_folder, settings = hypermea.jump_to_folder()
        hypermea.jump_back_to(starting_folder)
        return True
    except RuntimeError:
        return False


def _create_api(project_name):
    # TODO: ensure folder is empty? or at least warn if not?
    current_dir = os.getcwd()
    if project_name == '.':
        project_name = os.path.basename(os.getcwd())
    if _api_already_exist():
      click.echo('Please run in a folder that does not already contain an API service')
      return
    os.chdir(current_dir)
    click.echo(f'Creating {project_name} api')
    settings = {
        'project_name': project_name
    }
    with open('.hypermea', 'w') as f:
        json.dump(settings, f, indent=4)

    skel = os.path.join(os.path.dirname(hypermea.__file__), 'skel')
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
    hypermea.remove_folder_if_exists(os.path.join('scripts', '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, 'configuration', '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, 'domain', '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, 'hooks', '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, 'log_trace', '__pycache__'))
    hypermea.remove_folder_if_exists(os.path.join(project_name, 'utils', '__pycache__'))

    os.chdir('..')
    hypermea.replace_project_name(project_name, '.')


def _add_addins(which_addins, silent=False):
    try:
        starting_folder, settings = hypermea.jump_to_folder()
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1, silent)

    for keyword in [kw for kw in which_addins.keys() if which_addins[kw]]:
        addin_name = keyword[4:]  # remove "add-"
        settings_addins = settings.get('addins', {})
        if addin_name in settings_addins:
            if not silent: print(f'{addin_name} is already added.')
            hypermea.jump_back_to(starting_folder)
            return
        settings_addins[addin_name] = which_addins[keyword]
        settings = hypermea.add_to_settings('addins', settings_addins)

        if addin_name == 'git':
            continue

        addin_module = importlib.import_module(f'hypermea.addins.{addin_name}')
        add = getattr(addin_module, 'add')
        if which_addins[keyword] == 'n/a':
            add(silent)
        else:
            add(which_addins[keyword], silent)

    if which_addins.get('add_git', False):
        addins.git.add(which_addins['add_git'], silent)
        
    hypermea.jump_back_to(starting_folder)


def _show_or_set_version(new_version):
    if new_version == 'n/a':
        return hypermea.escape('The value for --set-version is not correct (e.g. --set-version=1.0.0)', 11)

    try:
        starting_folder, settings = hypermea.jump_to_folder('src/{project_name}/configuration')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    filename = '__init__.py'
    with open(filename, 'r') as f:
        lines = f.readlines()

    modified = ''
    starts_with = 'VERSION = '

    for line in lines:
        if line.startswith(starts_with):
            print(line.rstrip().lstrip())
            line = f'{starts_with}{new_version}\n'

        modified += line

    if new_version:
        print(f'- set to: {new_version}\n')
        with open(filename, 'w') as f:
            f.write(modified)
    else:
        print('- unchanged\n')
        
    hypermea.jump_back_to(starting_folder)
