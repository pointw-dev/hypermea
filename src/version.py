#! /usr/bin/env python

import os
import platform
import argparse
from datetime import date

# do not change version manually here, use this script which keeps
VERSION = '0.9.29'


def change_file(new_version, filename, starts_with, ends_with, change=True):
    with open(filename, 'r') as f:
        lines = f.readlines()
        
    moded = ''

    print(f'\n=== {filename}')
    for line in lines:
        if line.startswith(starts_with):
            new_line_ending = ends_with.format(version=new_version)
            print('current: ', line.rstrip())
            line = f"{starts_with}{new_line_ending}\n"
            print('updated: ', line.rstrip())

        moded += line
        
    if change:
        with open(filename, 'w') as f:
            f.write(moded)
    else:
        print(' - unchanged')


def main():
    print(f'Version is {VERSION}')

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--set', help='Provide the new version to set.')
    parser.add_argument('-d', '--dry-run', help='See which files will change, and from what version.', action='store_true')
    parser.add_argument('-t', '--tag', help='Create git tag with current version (ignored if used with --set).', action='store_true')

    files_to_modify = [
        {
            'path': './version.py',
            'line_starts_with': 'VERSION = ',
            'ends_with': "'{version}'"
        },        
        {
            'path': './hypermea/core/__init__.py',
            'line_starts_with': 'VERSION = ',
            'ends_with': "'{version}'"
        },
        {
            'path': './hypermea/tool/commands/__init__.py',
            'line_starts_with': 'VERSION = ',
            'ends_with': "'{version}'"
        },
        {
            'path': './hypermea/tool/skel/api/requirements.txt',
            'line_starts_with': 'hypermea-core==',
            'ends_with': '{version}'
        },
        {
            'path': '../jekyll/_includes/nav_footer_custom.html',
            'line_starts_with': '<p class="version-number">Version ',
            'ends_with': '{version}</p>'
        }
    ]

    args = parser.parse_args()

    current_version = VERSION

    new_version = args.set
    change = not args.dry_run
    if args.set:
        if args.dry_run:
            print('----- DRY RUN -----\n')
        print(f'Changing to {new_version}')
        for file in files_to_modify:
            change_file(new_version, file['path'], file['line_starts_with'], file['ends_with'], change)

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
