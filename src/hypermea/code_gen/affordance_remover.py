from libcst import *
from .file_transformer import FileTransformer


class AffordanceRemover(FileTransformer):
    def __init__(self, affordance_name, folder, singular):
        super().__init__()
        self.singular = singular
        self.affordance_name = affordance_name
        self.folder = folder
        self.affordance = f'affordances.{folder + "." if folder else ""}{affordance_name}'  # TODO: this is in multiple places

    def leave_FunctionDef(self, original_node, updated_node):
        """ Removes add_affordance() call from add_hooks, add_links() from  _add_links_to_singular():
        """

        fn = updated_node.name.value
        if fn not in ['add_hooks', f'_add_links_to_{self.singular}']:
            return updated_node

        new_body = []
        for item in updated_node.body.body:
            if (
                    fn == 'add_hooks'
                    and isinstance(item, SimpleStatementLine)
                    and isinstance(item.body[0], Expr)
                    and isinstance(item.body[0].value, Call)
                    and isinstance(item.body[0].value.func, Attribute)
                    and isinstance(item.body[0].value.func.value, Attribute)
                    and isinstance(item.body[0].value.func.value.value, Attribute)
                    and item.body[0].value.func.value.value.value.value == 'affordances'
                    and item.body[0].value.func.value.value.attr.value == self.folder
                    and item.body[0].value.func.value.attr.value == self.affordance_name
                ) or (
                    fn == f'_add_links_to_{self.singular}'
                    and isinstance(item, SimpleStatementLine)
                    and isinstance(item.body[0], Expr)
                    and isinstance(item.body[0].value, Call)
                    and isinstance(item.body[0].value.func, Attribute)
                    and isinstance(item.body[0].value.func.value, Attribute)
                    and isinstance(item.body[0].value.func.value.value, Attribute)
                    and item.body[0].value.func.value.value.value.value == 'affordances'
                    and item.body[0].value.func.value.value.attr.value == self.folder
                    and item.body[0].value.func.value.attr.value == self.affordance_name
            ):
                continue

            new_body.append(item)

        """
        (
                            fn == 'add_hooks'
                            and isinstance(item, SimpleStatementLine)
                            and isinstance(item.body[0], Expr)
                            and isinstance(item.body[0].value, Call)
                            and isinstance(item.body[0].value.func, Attribute)
                            and isinstance(item.body[0].value.func.value, Attribute)
                            and isinstance(item.body[0].value.func.value.value, Attribute)
                            and item.body[0].value.func.value.value.value.value == 'affordances'
                            and item.body[0].value.func.value.value.attr.value == self.folder
                            and item.body[0].value.func.value.attr.value == self.affordance_name
                    ) or """

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
