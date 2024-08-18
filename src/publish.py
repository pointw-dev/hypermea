#!/usr/bin/env python

import os
from build import main as build
import argparse
from version import VERSION


def publish_pypi(test=False):
    if not os.path.exists('./dist'):
        build()
        print()
        
    if test:
        print(f'Publishing {VERSION} to test.pypi.org')
        os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')
        print()
        print('install with:')
        print('  pip install libcst')
        print('  pip install inflect')
        print('  pip install --index-url https://test.pypi.org/simple/ hypermea')
    else:
        print(f'Publishing {VERSION} to pypi')
        os.system('twine upload dist/*')
        print()
        print('install with:')
        print('  pip install hypermea')
        print('upgrade with:')
        print('  pip install --upgrade hypermea')
    

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', help='Publish to test.pypi.org .', action='store_true')
    
    args = parser.parse_args()
    publish_pypi(args.test)
    

if __name__ == '__main__':
    main()
