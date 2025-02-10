import os
import platform
import subprocess
import re
import click


class DockerManager:
    def __init__(self, image_name, version=None, repository=None):
        self.image_name = image_name
        self.is_windows = platform.system() == 'Windows'
        self.silence = 'nul' if self.is_windows else '/dev/null'

    def build(self, version, repository):
        old_image_id = subprocess.getoutput(f'docker images {self.image_name}:{version} --quiet') if version else None

        errorlevel = os.system(f'docker build -t {self.image_name}:latest .')
        if errorlevel:
            click.echo('hypermea: error encountered building docker image.')
            quit(errorlevel)
        new_image_id = subprocess.getoutput(f'docker images {self.image_name}:latest --quiet')
        git_branch = subprocess.getoutput(f'git rev-parse --abbrev-ref HEAD 2>{self.silence}')

        tags = []
        if version:
            tags.append(f'{self.image_name}:{version}')
        if git_branch:
            tags.append(f'{self.image_name}:{git_branch}')
        if repository:
            tags.append(f'{repository}/{self.image_name}:latest')
            if version:
                tags.append(f'{repository}/{self.image_name}:{version}')
            if git_branch:
                tags.append(f'{repository}/{self.image_name}:{git_branch}')

        for tag in tags:
            os.system(f'docker tag {new_image_id} {tag}')

        if old_image_id and not old_image_id == new_image_id:
            repo_tags = subprocess.getoutput(f'docker inspect --format="{{{{.RepoTags}}}}" {old_image_id}')
            if repo_tags == '[]':
                click.echo(f'Cleaning up the image that used to be {version}.')
                os.system(f'docker image rm {old_image_id}')

    def _get_image_list(self):
        api_images = []
        all_images_list = subprocess.getoutput('docker image ls --format="{{.Repository}}:{{.Tag}}"').split('\n')
        for image in all_images_list:
            parts = re.split('/|:', image)
            if self.image_name in parts:
                api_images.append(image)
        return api_images

    def list(self):
        images = self._get_image_list()
        for image in images:
            click.echo(image)

    def wipe(self):
        to_delete = self._get_image_list()
        if not to_delete:
            click.echo('No images to delete')
            return

        for image in to_delete:
            os.system(f'docker rmi {image}')
