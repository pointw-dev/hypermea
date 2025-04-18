"""
ParentLinksInserter is invoked when a link is created and the child of the link is external.
It is therefore necessary to modify the hooks for the parent resource.

def _add_remote_children_links(person):
     if not SETTINGS['HY_GATEWAY_URL']:
         return
     person_id = get_resource_id(person, 'people')
+    person['_links']['hobbies'] = {
+        'href': f"{get_href_from_gateway('hobbies')}/person/{person_id}",
+        'title': 'hobbies'
+    }
"""

from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class ParentLinksInserter(FileTransformer):
    def __init__(self, adder):
        super().__init__()
        self.adder = adder

    def leave_FunctionDef(self, original_node, updated_node):
        if not self.adder.relation.child.external or not original_node.name.value == '_add_external_children_links':
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
                            Arg(SimpleString(f"'{self.adder.child}'"))
                        ]
                    )
                ),
                FormattedStringText(f'/{self.adder.parent}/'),
                FormattedStringExpression(expression=Name(f'{self.adder.parent}_id')),
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
            resource=self.adder.parent,
            rel=self.adder.child,
            href=self._get_href_value()
        )
