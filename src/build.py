#! /usr/bin/env python

import os
from shutil import copyfile
from clean import main as clean
from version import VERSION


def main():
    print(f'Building {VERSION}')
    clean()
    copyfile('../README.md', './README.md')
    os.system('python setup.py bdist_wheel')
    # os.system('python setup.py sdist bdist_wheel')  # TODO remove sdist if not Windows - or better fix the problem
    os.remove('./README.md')

if __name__ == '__main__':
    main()
