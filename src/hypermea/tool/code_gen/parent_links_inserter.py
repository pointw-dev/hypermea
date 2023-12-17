from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class ParentLinksInserter(FileTransformer):
    def __init__(self, adder):
        super().__init__()
        self.adder = adder

    def leave_FunctionDef(self, original_node, updated_node):
        method_name = '_add_remote_children_links' if self.adder.remote_child else f'_add_links_to_{self.adder.parent}'
        if not original_node.name.value == method_name:
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
                            Arg(SimpleString(f"'{self.adder.children}'"))
                        ]
                    )
                ),
                FormattedStringText(f'/{self.adder.parent}/'),
                FormattedStringExpression(expression=Name(f'{self.adder.parent}_id')),
            ],
            start='f"',
            end='"'
        ) if self.adder.remote_child else [
            FormattedStringText(f'/{self.adder.parents}/'),
            FormattedStringExpression(expression=Name(f'{self.adder.parent}_id')),
            FormattedStringText(f'/{self.adder.children}')
        ]

    def make_children_link(self):
        """ This adds the following to hooks.parents:_add_links_to_parent()
                parent['_links']['children'] = {
                 'href': f'/parents/{parent["_id"]}/children',
                 'title': 'children'
                }
            or this if the child is remote to hooks.parents:_add_remote_children_links()
                parent['_links']['children'] = {
                    'href': "{get_href_from_gateway('children')}/parents/parent['_id']/children',
                    'title': 'children'
                }
        """

        return code_gen.get_link_statement_line(
            resource=self.adder.parent,
            rel=self.adder.children,
            href=self._get_href_value(),
            title=self.adder.children
        )
