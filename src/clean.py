#!/usr/bin/env python

from shutil import rmtree

def silent_rmdir(path):
    try:
        rmtree(path)
    except FileNotFoundError:
        pass


def main():
    silent_rmdir('./dist')
    silent_rmdir('./build')
    silent_rmdir('./hypermea.egg-info')
    silent_rmdir('./hypermea_core.egg-info')
    silent_rmdir('./hypermea/hypermea_core.egg-info')
    silent_rmdir('./hypermea/core/hypermea_core.egg-info')
    
    
if __name__ == '__main__':
    main()
