import os
import signal
from hypermea_service import HypermeaService


def main():
    args = HypermeaService.parse_command_line_args()
    signal.signal(signal.SIGTERM, HypermeaService.stop_service_signal_handler)

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
