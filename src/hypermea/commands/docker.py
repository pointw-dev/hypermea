import os
import platform

import click
from .command_help_order import CommandHelpOrder
from .docker_manager import DockerManager  #, DockerManagerException
import hypermea


def _prepare_for_docker_command():
    try:
        starting_folder, settings = hypermea.jump_to_folder('src')
    except RuntimeError:
        return hypermea.escape('This command must be run in a hypermea folder structure', 1)

    if 'docker' not in settings.get('addins', {}):
        return hypermea.escape('This api does not have the docker addin installed.\n'
                               '- You can install docker with: hypermea api addin --add-docker', 2001)

    # DO NOT hypermea.jump_back_to(starting_folder)  - part of the preparation is to jump here
    return settings


@click.group(name='docker',
             help='Shortcuts to managing docker.',
             cls=CommandHelpOrder)
def commands():
    pass


@commands.command(name='build',
                  short_help=f'Builds (or rebuilds) a docker image.',
                  help_priority=1)
@click.option('--version', '-v',
              help='Set the version label to use for this docker image.',
              metavar='[version]')
@click.option('--repository', '-r',
              help='Set repository this image will be pushed to.',
              metavar='[repository]')
def build(version, repository):
    """
    Launches docker build, using the current version as a label (unless overriden by --version).
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    if not version:
        version = hypermea.get_api_version()

    docker_manager = DockerManager(image_name)
    docker_manager.build(version, repository)


@commands.command(name='list',
                  short_help=f'Lists the docker images built from this api.',
                  help_priority=2)
def list_images():
    """
    Lists the docker images:tags built with this api.
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    docker_manager = DockerManager(image_name)
    docker_manager.list()


@commands.command(name='wipe',
                  short_help=f'Deletes all docker images built from this api.',
                  help_priority=3)
def wipe():
    """
    Deletes all docker images build from this api.
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    docker_manager = DockerManager(image_name)
    docker_manager.wipe()


@commands.command(name='up',
                  short_help=f'Runs `docker compose up -d`',
                  help_priority=4)
@click.argument('suffix', metavar='[suffix]', default='none')
def up(suffix):
    """
    Runs `docker compose up -d` using this api's docker-compose.yml

    pass a suffix to use docker-compose.{suffix}.yml instead.
    """
    _prepare_for_docker_command()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'
    os.system(f'docker compose {file_parameter} up -d')


@commands.command(name='down',
                  short_help=f'Runs `docker compose down`',
                  help_priority=5)
@click.argument('suffix', metavar='[suffix]', default='none')
def down(suffix):
    """
    Runs `docker compose down`

    pass a suffix to use docker-compose.{suffix}.yml instead.
    """
    _prepare_for_docker_command()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'
    os.system(f'docker compose {file_parameter} down')


@commands.command(name='cycle',
                  short_help=f'The same as down, wipe, build, up',
                  help_priority=6)
@click.argument('suffix', metavar='[suffix]', default='none')
def cycle(suffix):
    """
    Runs hypermea docker down / wipe / build / up

    pass a suffix to run docker-compose.{suffix}.yml instead.
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']
    docker_manager = DockerManager(image_name)
    version = hypermea.get_api_version()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'

    click.echo(f"-- docker down {'' if suffix == 'none' else suffix + ' ' }--")
    os.system(f'docker compose {file_parameter} down')

    click.echo('-- docker wipe --')
    docker_manager.wipe()

    click.echo('-- docker build --')
    docker_manager.build(version, None)

    click.echo(f"-- docker up {'' if suffix == 'none' else suffix + ' ' }--")
    os.system(f'docker compose {file_parameter} up -d')


@commands.command(name='logs',
                  short_help=f'Shows docker logs for the running api.',
                  help_priority=7)
@click.option('--follow', '-f',
              is_flag=True, help='Follow log output')
@click.option('--popup', '-p',
              is_flag=True, help='Launch log in popup (assumes --follow)')
def logs(follow, popup):
    """
    Shows (and optionally follows) the docker log for the running api.
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']
    command = f'docker logs {image_name} {"--follow" if follow or popup else ""}'

    if popup:
        if platform.system() != 'Windows':
            click.echo('popups for your platform are not yet supported')
        else:
            title = f"{settings['project_name']} - docker logs --follow"
            command = f"start \"{title}\" {command}"
    os.system(command)
