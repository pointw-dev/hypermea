from libcst import *
from .file_transformer import FileTransformer


class AffordanceRouteRemover(FileTransformer):
    def __init__(self, affordance, singular):
        super().__init__()
        self.singular = singular
        self.affordance = affordance

    def leave_Module(self, original_node, updated_node):
        new_body = []
        for item in updated_node.body:
            if isinstance(item, FunctionDef) and item.name.value == f'_do_{self.affordance.identifier}_{self.singular}':
                continue
            new_body.append(item)

        return updated_node.with_changes(
            body=new_body
        )

    def leave_FunctionDef(self, original_node, updated_node):
        """ Removes the route to /plural/singular_id/affordance from affordance.py:
        """

        if not original_node.name.value == 'add_affordance':
            return original_node

        new_body = []
        for item in updated_node.body.body:
            if isinstance(item, FunctionDef) and item.name.value == f'do_{self.affordance.identifier}_{self.singular}':
                continue
            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
