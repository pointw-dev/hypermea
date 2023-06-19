from libcst import *
from .file_transformer import FileTransformer


class ParentReferenceRemover(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def visit_Assign(self, node):
        if not node.targets[0].target.value == 'SCHEMA':
            return False

    def leave_DictElement(self, original_node, updated_node):
        skip_it = True
        if isinstance(original_node.value, Dict):
            for element in original_node.value.elements:
                if element.key.value in ["'data_relation'", "'remote_relation'"]:
                    skip_it = False
                    break
        if skip_it:
            return original_node

        remove = False

        for element in original_node.value.elements:
            if element.key.value not in ["'data_relation'", "'remote_relation'"]:
                continue
            for sub_element in element.value.elements:   # TODO: is this universally safe?
                if sub_element.value.value[1:-1] == self.resource:
                    remove = True

        return RemoveFromParent() if remove else original_node
