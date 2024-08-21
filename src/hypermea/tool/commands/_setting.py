import click


def _create():
    with open('schnizzel.txt', 'w') as f:
        f.write('Hello, world!\n')
    click.echo('create')


def _list_setting():
    click.echo('list')


def _remove():
    click.echo('remove')
