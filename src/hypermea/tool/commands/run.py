import click


@click.command(name='run', help='Launch the service.')
@click.option('--host',
              help='The interface to bind to.  Default is "0.0.0.0" which lets you call the API from a '
                   'remote location.  Use "localhost" to only allow calls from this location',
              metavar='[host]')
@click.option('--debug', '-d', is_flag=True, help='Turn on debugger, which enables auto-reload.', metavar='[debug]')
@click.option('--single-threaded', '-s', is_flag=True, help='Disables multithreading.', metavar='[single-threaded]')
def commands(host, debug, single_threaded):
    from ._run import _run
    return _run(host, debug, single_threaded)
