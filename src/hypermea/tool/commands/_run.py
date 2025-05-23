import os
import platform

import hypermea.tool


def _run(host, debug, single_threaded):
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src/service')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    try:
        import dotenv
    except ModuleNotFoundError:
        # TODO: ask first?
        os.system('pip install -r requirements.txt')

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
