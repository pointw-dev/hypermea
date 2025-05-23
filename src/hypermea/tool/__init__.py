import os
import sys
import subprocess
import json
from pathlib import Path
from shutil import copytree, rmtree, ignore_patterns


def jump_to_folder(path=None):
    starting_folder = os.getcwd()
    while True:
        if os.path.isfile('.hypermea'):
            break

        current_dir = os.getcwd()
        if os.path.isdir('..'):
            os.chdir('..')
            if os.getcwd() == current_dir:
                jump_back_to(starting_folder)
                raise RuntimeError('Not in a hypermea folder')
        else:
            jump_back_to(starting_folder)
            raise RuntimeError('Not in a hypermea folder')

    with open('.hypermea', 'r') as f:
        settings = json.load(f)

    if path:
        os.chdir(path)

    return starting_folder, settings


def jump_back_to(starting_folder):
    os.chdir(starting_folder)


def get_settings():
    try:
        starting_folder, settings = jump_to_folder()
    except RuntimeError:
        return escape('This command must be run in a hypermea folder structure', 1)

    jump_back_to(starting_folder)
    return settings


def get_service_version():
    try:
        starting_folder, settings = jump_to_folder('src/service')
    except RuntimeError:
        return escape('This command must be run in a hypermea folder structure', 1)

    with open('__init__.py', 'r') as f:
        lines = f.readlines()

    version = 'unknown_version'
    starts_with = 'VERSION = '

    for line in lines:
        if line.startswith(starts_with):
            version = line.split(' = ')[1].strip().replace("'", '').replace('"', '')
            break

    jump_back_to(starting_folder)
    return version


def add_to_settings(key, value):
    try:
        starting_folder, settings = jump_to_folder()
    except RuntimeError:
        return escape('This command must be run in a hypermea folder structure', 1)

    settings[key] = value

    with open('.hypermea', 'w') as f:
        to_write = json.dumps(settings) + '\n'
        f.write(to_write)
    jump_back_to(starting_folder)
    return settings


def install_packages(packages, command):
    trigger = 'Successfully installed '
    subprocess.check_output([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

    with open('requirements.txt', 'a') as f:
        f.write(f'\n# start: added by {command}\n')
        for package in packages:
            subprocess.check_output([sys.executable, '-m', 'pip', 'install', package]).decode('utf-8')
            out = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
            for line in out.split('\n'):
                if package in line:
                    f.write(f'{line.strip()}\n')

        f.write(f'# end: added by {command}\n')


def run_setup(integration, silent=False):
    from hypermea.core.utils import import_module_from_path
    try:
        filename = os.path.join(os.path.dirname(__file__), f'skel/integration/{integration}', '_setup.py')
        integration_module = import_module_from_path(integration, filename)
        integration_setup = getattr(integration_module, 'setup', None)
    except FileNotFoundError:
        integration_setup = None
    if integration_setup:
        integration_setup()



def copy_skel(project_name, skel_folder, target_folder=None, replace=None, silent=False):
    if not silent: print(f'Adding {skel_folder} to {project_name} service')

    source = os.path.join(os.path.dirname(__file__), f'skel/{skel_folder}')
    destination = skel_folder if not target_folder else target_folder

    if not target_folder:
        if not os.path.isdir(skel_folder):
            os.mkdir(skel_folder)  # TODO: ensure doesn't already exist, etc
    copytree(source, destination, dirs_exist_ok=True,
        ignore=ignore_patterns(
            '__pycache__',
            '*.pyc',
            '_setup.py'
        )
    )

    # TODO: can the following remove_tree calls be obviated if skel is packaged differently?
    for pycache_dir in Path(destination).rglob('__pycache__'):
        rmtree(pycache_dir)

    if replace is None:
        replace = {}
    replace['project_name'] = project_name

    for item in replace:
        for dname, dirs, files in os.walk(destination):
            for fname in files:
                fpath = os.path.join(dname, fname)
                if fname.endswith('.pyc') or fname.endswith('.ico'):
                    continue
                with open(fpath, 'r') as f:
                    try:
                        s = f.read()
                    except UnicodeDecodeError as ex:
                        continue
                changed = False
                if f'{{${item}}}' in s:
                    s = s.replace(f'{{${item}}}', replace[item])
                    changed = True
                if changed:
                    with open(fpath, 'w') as f:
                        f.write(s)


def replace_project_name(project_name, folder):
    # TODO: jinja?
    for dname, dirs, files in os.walk(folder):
        for fname in files:
            # do not process if traversing nested venv folder
            if os.path.abspath(dname).startswith(sys.prefix):
              continue
            if '__pycache__' in dname:
              continue
            if '.idea' in dname and 'icon' in fname:
              continue
            if 'favicon' in fname:
              continue
            fpath = os.path.join(dname, fname)
            try:
              with open(fpath) as f:
                  s = f.read()
              s = s.replace('{$project_name}', project_name)
              with open(fpath, 'w') as f:
                  f.write(s)
            except UnicodeDecodeError as ex:
              print(f'Skipping unprocessable file: {dname}/{fname}')


def remove_file_if_exists(filename):
    if os.path.exists(filename):
        os.remove(filename)


def remove_folder_if_exists(root_folder, folder_to_delete, recursive=False):
    if recursive:
        for dir_name, _, _ in os.walk(root_folder):
            remove_folder_if_exists(dir_name, folder_to_delete)
    else:
        path_to_delete = os.path.join(root_folder, folder_to_delete)
        if os.path.exists(path_to_delete):
            rmtree(path_to_delete)


def escape(message, code, silent=False):
    if silent:
        return code
    print(message)
    sys.exit(code)


def urljoin(*parts):
    trailing_slash = '/' if parts[-1].endswith('/') else ''
    return '/'.join([str(part).strip('/') for part in parts]) + trailing_slash
