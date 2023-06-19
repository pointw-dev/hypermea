from libcst import *
from .file_transformer import FileTransformer


class AffordanceImportRemover(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_ImportFrom(self, original_node, updated_node):
        """ Removes the following to the top of domain/__init__.py:
               from . import resource
        """
        if original_node.names[0].name.value == self.resource:
            return RemoveFromParent()

        return original_node
