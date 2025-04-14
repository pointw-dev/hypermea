#!/usr/bin/env python

import sys
from hypermea.tool import get_singular_plural

def main():
    if len(sys.argv) < 2:
        print('USAGE: singplu word')
        quit(1)

    word = sys.argv[1]
    singular, plural = get_singular_plural(word)

    print(word)
    print(f' - one  {singular}')
    print(f' - many {plural}')


if __name__ == '__main__':
    main()
