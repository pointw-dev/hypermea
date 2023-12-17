import os
import platform

import hypermea.tool


def _run(host, debug, single_threaded):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        import eve
        import cerberus
    except ModuleNotFoundError:
        # TODO: ask first?
        os.system('pip install -r requirements.txt')

    # TODO: warn if mongo is not running at localhost:27017

    command = 'python run.py'
    if platform.system() == 'Windows':
        title = f"{settings['project_name']}"
        args = ' '
        if host:
            args += f'--host={host} '
            title += f' - {host}'
        if debug:
            args += f'--debug '
            title += ' - DEBUG/RELOAD ENABLED'
        if single_threaded:
            args += f'--single_threaded'

        print(args)
        command = f"start \"{title}\" python run.py {args}"

    os.system(command)
    hypermea.tool.jump_back_to(starting_folder)
