from libcst import *
from .file_transformer import FileTransformer


class DomainResourceRemover(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_ImportFrom(self, original_node, updated_node):
        """ Removes the following to the top of domain/__init__.py:
               from . import resource
        """
        if original_node.names[0].name.value == self.resource:
            return  RemoveFromParent()

        return original_node

    def visit_Assign(self, node):
        if not node.targets[0].target.value in ['DOMAIN_DEFINITIONS', 'DOMAIN_RELATIONS']:
            return False

    def leave_DictElement(self, original_node, updated_node):
        key = original_node.key.value[1:-1]
        if key == self.resource:
            return RemoveFromParent()

        if self.resource in key.split('_'):
            return RemoveFromParent()

        return original_node
