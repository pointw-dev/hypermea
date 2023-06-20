import os
import click
import platform
import hypermea


@click.command(name='run', help='Launch the service.')
@click.option('--host',
              help='The interface to bind to.  Default is "0.0.0.0" which lets you call the API from a '
                   'remote location.  Use "localhost" to only allow calls from this location',
              metavar='[host]')
@click.option('--debug', '-d', is_flag=True, help='Turn on debugger, which enables auto-reload.', metavar='[debug]')
@click.option('--single-threaded', '-s', is_flag=True, help='Disables multithreading.', metavar='[single-threaded]')
def commands(host, debug, single_threaded):
    try:
        starting_folder, settings = hypermea.jump_to_folder('src/{project_name}')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)
        
    try:
        import eve
        import cerberus
    except ModuleNotFoundError:
        # TODO: ask first?
        os.system('pip install -r requirements.txt')

    # TODO: warn if mongo is not running at localhost:27017
        
    cmd = 'python run.py'    
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
        cmd = f"start \"{title}\" python run.py {args}"

    os.system(cmd)
    hypermea.jump_back_to(starting_folder)

