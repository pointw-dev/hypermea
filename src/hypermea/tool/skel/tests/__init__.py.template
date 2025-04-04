import logging
from types import SimpleNamespace, ModuleType
from .annotate import annotated_scenario

LOG = logging.getLogger('test-suite')


def load_settings_from_file(filename):
    d = ModuleType('settings')
    with open(filename) as f:
        exec(f.read(), d.__dict__)
    return {k: v for k, v in d.__dict__.items() if k.isupper()}


def display(message, title=None):
    print('\n\n==========')
    if title:
        print(f'-- {title}')
    print(message)
    print('==========\n\n')
