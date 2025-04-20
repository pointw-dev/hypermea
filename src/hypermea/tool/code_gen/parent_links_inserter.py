"""
ParentLinksInserter is invoked when a link is created and the child of the link is external.
It is therefore necessary to modify the hooks for the parent resource.

def _add_external_children_links({parent}):
     if not SETTINGS['HY_GATEWAY_URL']:
         return
     {parent}_id = get_resource_id({parent}, '{parents}')
+    {parent}['_links']['{child}'] = {
+        'href': f"{get_href_from_gateway('{child}')}/{parent}/{{ {parent}_id }}",
+    }
"""

from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class ParentLinksInserter(FileTransformer):
    def __init__(self, link_manager):
        super().__init__()
        self.lm = link_manager

    def leave_FunctionDef(self, original_node, updated_node):
        if not self.lm.relation.child.external or not original_node.name.value == '_add_external_children_links':
            return original_node

        new_body = []
        for item in original_node.body.body:
            new_body.append(item)
        new_body.append(self.make_children_link())

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )

    def _get_href_value(self):
        return FormattedString(
            parts=[
                FormattedStringExpression(
                    expression=Call(
                        func=Name('get_href_from_gateway'),
                        args=[
                            Arg(SimpleString(f"'{self.lm.child}'"))
                        ]
                    )
                ),
                FormattedStringText(f'/{self.lm.parent}/'),
                FormattedStringExpression(expression=Name(f'{self.lm.parent}_id')),
            ],
            start='f"',
            end='"'
        )

    def make_children_link(self):
        """ This adds the following to hooks.parents:_add_external_children_links()
                parent['_links']['child'] = {
                    'href': "{get_href_from_gateway('child')}/parents/parent['_id']/children'
                }
        """

        return code_gen.get_link_statement_line(
            resource=self.lm.parent,
            rel=self.lm.child,
            href=self._get_href_value()
        )
