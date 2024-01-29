import os
import platform

import click

import hypermea.tool
from hypermea.tool.commands.docker_manager import DockerManager


def _prepare_for_docker_command():
    try:
        starting_folder, settings = hypermea.tool.jump_to_folder('src')
    except RuntimeError:
        return hypermea.tool.escape('This command must be run in a hypermea folder structure', 1)

    if 'docker' not in settings.get('addins', {}):
        return hypermea.tool.escape('This api does not have the docker addin installed.\n'
                               '- You can install docker with: hypermea api addin --add-docker', 2001)

    # DO NOT hypermea.jump_back_to(starting_folder)  - part of the preparation is to jump here
    return settings


def _build(version, repository):
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    if not version:
        version = hypermea.tool.get_api_version()

    docker_manager = DockerManager(image_name)
    docker_manager.build(version, repository)


def _list_images():
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    docker_manager = DockerManager(image_name)
    docker_manager.list()


def _wipe():
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']

    docker_manager = DockerManager(image_name)
    docker_manager.wipe()


def _start():
    settings = _prepare_for_docker_command()
    container_name = settings['project_name']
    os.system(f'docker start {container_name}')


def _stop():
    settings = _prepare_for_docker_command()
    container_name = settings['project_name']
    os.system(f'docker stop {container_name}')


def _up(suffix):
    _prepare_for_docker_command()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'
    os.system(f'docker compose {file_parameter} up -d')


def _down(suffix):
    _prepare_for_docker_command()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'
    os.system(f'docker compose {file_parameter} down')


def _cycle(suffix):
    settings = _prepare_for_docker_command()
    image_name = settings['project_name']
    docker_manager = DockerManager(image_name)
    version = hypermea.tool.get_api_version()
    file_parameter = '' if suffix == 'none' else f'-f docker-compose.{suffix}.yml'

    click.echo(f"-- docker down {'' if suffix == 'none' else suffix + ' ' }--")
    os.system(f'docker compose {file_parameter} down')

    click.echo('-- docker wipe --')
    docker_manager.wipe()

    click.echo('-- docker build --')
    docker_manager.build(version, None)

    click.echo(f"-- docker up {'' if suffix == 'none' else suffix + ' ' }--")
    os.system(f'docker compose {file_parameter} up -d')


def _logs(follow, popup):
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
