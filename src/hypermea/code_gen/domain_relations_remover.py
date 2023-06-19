from libcst import *
from .file_transformer import FileTransformer


class DomainRelationsRemover(FileTransformer):
    def __init__(self, parents, children):
        super().__init__()
        self.key = f'{parents}_{children}'

    def visit_Assign(self, node):
        if not node.targets[0].target.value in ['DOMAIN_RELATIONS']:
            return False

    def leave_DictElement(self, original_node, updated_node):
        key = original_node.key.value[1:-1]
        if key == self.key:
            return RemoveFromParent()

        return original_node
