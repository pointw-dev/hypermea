import sys

from libcst import *
from .file_transformer import FileTransformer


class DomainRelationsRemover(FileTransformer):
    def __init__(self, relation):
        super().__init__()
        self.relation = relation

    def leave_Element(self, original_node, updated_node):
        try:
            from hypermea.core.domain import Relation, external, local  # safe eval context
            node_code = Module([]).code_for_node(updated_node).strip()
            if node_code[-1] == ',':
                node_code = node_code[:-1]
            candidate = eval(node_code)
            if candidate == self.relation:
                return RemoveFromParent()
        except Exception as e:
            import traceback
            print(''.join(traceback.format_exception(e)))

        return updated_node