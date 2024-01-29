import click
from .command_help_order import CommandHelpOrder


@click.group(name='docker',
             help='Shortcuts to managing docker.',
             cls=CommandHelpOrder)
def commands():
    # This method is empty as it is a group in which the following commands are inserted
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
    from ._docker import _build
    return _build(version, repository)


@commands.command(name='list',
                  short_help=f'Lists the docker images built from this api.',
                  help_priority=2)
def list_images():
    """
    Lists the docker images:tags built with this api.
    """
    from ._docker import _list_images
    return _list_images()


@commands.command(name='wipe',
                  short_help=f'Deletes all docker images built from this api.',
                  help_priority=3)
def wipe():
    """
    Deletes all docker images build from this api.
    """
    from ._docker import _wipe
    return _wipe()


@commands.command(name='start',
                  short_help=f'Starts the api container, leaving other containers running.',
                  help_priority=4)
def start_container():
    """
    Deletes all docker images build from this api.
    """
    from ._docker import _start
    return _start()


@commands.command(name='stop',
                  short_help=f'Stops the api container, leaving other containers running.',
                  help_priority=5)
def stop_container():
    """
    Deletes all docker images build from this api.
    """
    from ._docker import _stop
    return _stop()


@commands.command(name='up',
                  short_help=f'Runs `docker compose up -d`',
                  help_priority=6)
@click.argument('suffix', metavar='[suffix]', default='none')
def up(suffix):
    """
    Runs `docker compose up -d` using this api's docker-compose.yml

    pass a suffix to use docker-compose.{suffix}.yml instead.
    """
    from ._docker import _up
    return _up(suffix)


@commands.command(name='down',
                  short_help=f'Runs `docker compose down`',
                  help_priority=7)
@click.argument('suffix', metavar='[suffix]', default='none')
def down(suffix):
    """
    Runs `docker compose down`

    pass a suffix to use docker-compose.{suffix}.yml instead.
    """
    from ._docker import _down
    return _down(suffix)


@commands.command(name='cycle',
                  short_help=f'The same as down, wipe, build, up',
                  help_priority=8)
@click.argument('suffix', metavar='[suffix]', default='none')
def cycle(suffix):
    """
    Runs hypermea docker down / wipe / build / up

    pass a suffix to run docker-compose.{suffix}.yml instead.
    """
    from ._docker import _cycle
    return _cycle(suffix)


@commands.command(name='logs',
                  short_help=f'Shows docker logs for the running api.',
                  help_priority=9)
@click.option('--follow', '-f',
              is_flag=True, help='Follow log output')
@click.option('--popup', '-p',
              is_flag=True, help='Launch log in popup (assumes --follow)')
def logs(follow, popup):
    """
    Shows (and optionally follows) the docker log for the running api.
    """
    from ._docker import _logs
    return _logs(follow, popup)
