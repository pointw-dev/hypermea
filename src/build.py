#!/usr/bin/env python

import os
from shutil import copyfile
from clean import main as clean
from version import VERSION


def main():
    print(f'Building {VERSION}')
    clean()
    os.system('python setup-core.py bdist_wheel')
    os.system('python setup-tool.py bdist_wheel')
    # os.system('python setup.py sdist bdist_wheel')  # TODO remove sdist if not Windows - or better fix the problem


if __name__ == '__main__':
    main()
