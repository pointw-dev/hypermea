import sys
from libcst import *

if len(sys.argv) < 2:
    print('USAGE: src_to_cst.py <python file>')
    quit(1)

with open(sys.argv[1], 'r') as source:
    tree = parse_module(source.read())
    
print(tree)
