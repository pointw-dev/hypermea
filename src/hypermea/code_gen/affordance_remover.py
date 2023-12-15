from libcst import *
from .file_transformer import FileTransformer


class AffordanceRemover(FileTransformer):
    def __init__(self, affordance, singular):
        super().__init__()
        self.singular = singular
        self.affordance = affordance

    def leave_FunctionDef(self, original_node, updated_node):
        """ Removes add_affordance() call from add_hooks, add_links() from  _add_links_to_singular():
        """

        fn = updated_node.name.value
        if fn not in ['add_hooks', f'_add_links_to_{self.singular}']:
            return updated_node

        new_body = []
        for item in updated_node.body.body:
            if self._should_this_be_removed(item):
                continue

            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )

    def _should_this_be_removed(self, item):
        rtn = isinstance(item, SimpleStatementLine) \
              and isinstance(item.body[0], Expr) \
              and isinstance(item.body[0].value, Call) \
              and isinstance(item.body[0].value.func, Attribute) \
              and isinstance(item.body[0].value.func.value, Attribute)

        if self.affordance.folder:
            rtn = rtn and isinstance(item.body[0].value.func.value.value, Attribute) \
                  and item.body[0].value.func.value.value.value.value == 'affordances' \
                  and item.body[0].value.func.value.value.attr.value == self.affordance.folder \
                  and item.body[0].value.func.value.attr.value == self.affordance.name
        else:
            rtn = rtn and item.body[0].value.func.value.value.value == 'affordances' \
                  and item.body[0].value.func.value.attr.value == self.affordance.name

        return rtn
