import os
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
def up():
    """
    Runs `docker compose up -d` using this api's docker-compose.yml
    """
    _prepare_for_docker_command()
    os.system('docker compose up -d')


@commands.command(name='down',
                  short_help=f'Runs `docker compose down`',
                  help_priority=5)
def down():
    """
    Runs `docker compose down`
    """
    _prepare_for_docker_command()
    os.system('docker compose down')


@commands.command(name='cycle',
                  short_help=f'The same as down, wipe, build, up',
                  help_priority=6)
def cycle():
    """
    Runs hypermea docker down / wipe / build / up
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']
    docker_manager = DockerManager(image_name)
    version = hypermea.get_api_version()

    click.echo('-- docker down --')
    os.system('docker compose down')
    click.echo('-- docker wipe --')
    docker_manager.wipe()
    click.echo('-- docker build --')
    docker_manager.build(version, None)
    click.echo('-- docker up --')
    os.system('docker compose up -d')


@commands.command(name='logs',
                  short_help=f'Shows docker logs for the running api.',
                  help_priority=7)
@click.option('--follow', '-f',
              is_flag=True, help='Follow log output')
def logs(follow):
    """
    Shows (and optionally follows) the docker log for the running api.
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    os.system(f'docker logs {image_name} {"--follow" if follow else ""}')
