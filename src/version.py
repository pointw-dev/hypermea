#! /usr/bin/env python

import os
import platform
import argparse
from datetime import date


# do not change version manually here, use this script which keeps hypermea in sync
VERSION = '0.9.21'


def main():
    print(f'Version is {VERSION}')

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', help='Provide the new version to set.')
    parser.add_argument('-t', '--tag', help='Create git tag with current version (ignored if used with --set).', action='store_true')


    args = parser.parse_args()

    current_version = VERSION

    if args.set:
        new_version = args.set
        print(f'Changing to {new_version}')

        with open('version.py', 'r') as f:
            lines = f.readlines()

        with open('version.py', 'w') as f:
            for line in lines:
                if line.startswith("VERSION = '"):
                    line = f"VERSION = '{new_version}'\n"
                f.write(line)

        current_version = new_version
    elif args.tag:  # cannot tag when file is freshly changed - must add/commit first
        print(f'creating git tag {current_version}')
        today = date.today()
        silent = ' > /dev/null 2> /dev/null'
        if platform.system() == 'Windows':
            silent = ' > nul 2> nul'

        comment = f'Released {today}'
        os.system(f'git tag -d {current_version} {silent}')
        os.system(f'git tag -a {current_version} -m "{comment}"')


if __name__ == '__main__':
    main()
