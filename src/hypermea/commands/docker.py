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

    # DO NOT  hypermea.jump_back_to(starting_folder)  - part of the preparation is to jump here
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
                  short_help=f'Lists all docker images built from this api.',
                  help_priority=2)
def list_images():
    """
    Launches docker build, using the current version as a label (unless overriden by --version).
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
    Launches docker build, using the current version as a label (unless overriden by --version).
    """
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    docker_manager = DockerManager(image_name)
    docker_manager.wipe()

