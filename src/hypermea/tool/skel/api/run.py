import os
import argparse
import signal
from hypermea_service import HypermeaService


def stop_api(signum, frame):  # pylint: disable=unused-argument
    """ Catches SIGTERM and issues SIGINT """
    if signum == signal.SIGTERM:
        os.kill(os.getpid(), signal.SIGINT)


def main():
    parser = argparse.ArgumentParser('{$project_name}', 'HypermeaService API')
    parser.add_argument('--host', help='The interface to bind to.  Default is "0.0.0.0" which lets you call the API from a remote location.  Use "localhost" to only allow calls from this location', default='0.0.0.0')
    parser.add_argument('-d', '--debug', help='Turn on debugger, which enables auto-reload.', action='store_true')
    parser.add_argument('-s', '--single-threaded', help='Disables multithreading.', action='store_true')
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, stop_api)

    kwargs = {
        'host': args.host
    }
    if args.debug:
        kwargs['debug'] = 'Enabled'

    if args.single_threaded:
        kwargs['threaded'] = 'Disabled'

    service = HypermeaService(**kwargs)

    try:
        service.start()
    except KeyboardInterrupt:
        service.stop()


if __name__ == '__main__':
    main()
