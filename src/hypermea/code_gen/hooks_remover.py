from libcst import *
from .file_transformer import FileTransformer


class HooksRemover(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_Import(self, original_node, updated_node):
        """ Removes the following to the top of hooks/__init__.py:
               import hooks.resource
        """
        node = updated_node.names[0].name
        if not isinstance(node, Attribute):
            return updated_node

        if node.attr.value == self.resource:
            return RemoveFromParent()

        return updated_node

    # TODO: why does this result in "TypeError: We got a RemovalSentinel while visiting a Call. This node's parent does not allow it to be removed." ???
    #       have to reshape the function definition instead :-(  (see leave_FunctionDef)
    # def leave_Call(self, original_node, updated_node):
    #     node = updated_node.func.value
    #     if not isinstance(node, Attribute):
    #         return updated_node
    #
    #     if node.value.value == 'hooks' and node.attr.value == self.resource:
    #         return RemoveFromParent()
    #
    #     return updated_node

    def leave_FunctionDef(self, original_node, updated_node):
        if not original_node.name.value == 'add_hooks':
            return original_node
        new_body = []
        for item in original_node.body.body:
            if isinstance(item, SimpleStatementLine) \
                    and isinstance(item.body[0], Expr) \
                    and isinstance(item.body[0].value, Call)\
                    and isinstance(item.body[0].value.func, Attribute)\
                    and isinstance(item.body[0].value.func.value, Attribute)\
                    and item.body[0].value.func.value.attr.value == self.resource:
                continue
            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
