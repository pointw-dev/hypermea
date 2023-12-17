from libcst import *
from .file_transformer import FileTransformer
##### import hypermea


class ChildLinksRemover(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_Assign(self, original_node, updated_node):
        target = original_node.targets[0].target
        if not isinstance(target, Subscript) or target.slice[0].slice.value.value[1:-1] != self.resource:
            return original_node

        return RemoveFromParent()

    def leave_FunctionDef(self, original_node, updated_node):
        fn = updated_node.name.value
        if fn != 'add_hooks' and (not fn.startswith('_add_links_to') or 'collection' in fn):
            return updated_node

        new_body = []
        for item in updated_node.body.body:
            if (
                    fn == 'add_hooks' and
                    isinstance(item, SimpleStatementLine)
                    and isinstance(item.body[0], AugAssign)
                    and isinstance(item.body[0].target, Attribute)
                    and self.resource in item.body[0].target.attr.value
            ) or (
                    fn.startswith('_add_links_to') and 'collection' not in fn
                    and isinstance(item, If)
                    and self.resource in f'{item}'
            ):
                continue
            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
