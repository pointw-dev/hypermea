from libcst import *


class FileTransformer(CSTTransformer):
    def __init__(self):
        super().__init__()

    def transform(self, filename):
        with open(filename, 'r') as source:
            tree = parse_module(source.read())

        new_tree = tree.visit(self)

        with open(filename, 'w') as source:
            source.write(new_tree.code)
