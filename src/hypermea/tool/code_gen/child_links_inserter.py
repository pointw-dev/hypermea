"""
ChildLinksInserter is invoked when a link is created.
It is therefore necessary to modify the hooks for the child resource.
How and what are modified depends on whether the parent relation is external.

IF THE PARENT IS EXTERNAL
def _add_remote_parent_links(person):
     if not SETTINGS['HY_GATEWAY_URL']:
         return
     person_id = get_resource_id(person, 'people')
+    if '_{parent}_ref' in person:
+        {child}['_links']['{parent}'] = {
+            'href': f"{get_href_from_gateway('{parent}')}/{{child}['_{parent}_ref']}"
+        }

IF THE PARENT IS NOT EXTERNAL
def add_hooks(app):
+    app.on_fetched_item_{parents}_{children} += _add_links_to_{child}
+    app.on_fetched_resource_{parents}_{children} += _add_links_to_{children}_collection
+    app.on_post_POST_{parents}_{children} += _post_{children}
"""

from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class ChildLinksInserter(FileTransformer):
    def __init__(self, link_manager):
        super().__init__()
        self.lm = link_manager

    def leave_FunctionDef(self, original_node, updated_node):
        method_name = '_add_external_parent_links'
        if not original_node.name.value in [method_name, 'add_hooks']:
            return original_node

        new_body = []
        for item in original_node.body.body:
            new_body.append(item)

        if original_node.name.value == method_name:
            pass
            new_body.append(self.make_external_parent_link())
        if original_node.name.value == 'add_hooks' and not self.lm.relation.parent.external:
            new_body.extend(self.add_rel_hooks())

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )

    def make_external_parent_link(self):
        href = FormattedString(
            parts=[
                FormattedStringExpression(
                    expression=Call(
                        func=Name('get_href_from_gateway'),
                        args=[
                            Arg(SimpleString(f"'{self.lm.relation.parent}'"))
                        ]
                    )
                ),
                FormattedStringText('/'),
                FormattedStringExpression(
                    expression=Subscript(
                        value=Name(str(self.lm.relation.child)),
                        slice=[
                            SubscriptElement(
                                slice=Index(SimpleString(f"'_{self.lm.relation.parent}_ref'"))
                            )
                        ],
                        lbracket=LeftSquareBracket(),
                        rbracket=RightSquareBracket()
                    )
                )
            ],
            start='f"',
            end='"'
        )
        additional_link = code_gen.get_link_statement_line(
            resource=str(self.lm.relation.child),
            rel=str(self.lm.relation.parent),
            href=href,
        )

        return If(
            test=Comparison(
                left=SimpleString(f"'_{self.lm.relation.parent}_ref'"),
                comparisons=[
                    ComparisonTarget(
                        operator=In(
                            whitespace_before=SimpleWhitespace(' '),
                            whitespace_after=SimpleWhitespace(' ')
                        ),
                        comparator=Name(str(self.lm.relation.child))
                    )
                ]
            ),
            body=IndentedBlock(
                body=[
                    additional_link
                ],
                header=code_gen.TWNL),
            orelse=None,
            whitespace_before_test=SimpleWhitespace(' ')
        )



    def add_rel_hooks(self):
        # Create the first SimpleStatementLine with the on_fetched_item hook.
        on_fetched_item_line = SimpleStatementLine(
            body=[
                AugAssign(
                    target=Attribute(
                        value=Name('app'),
                        attr=Name(f'on_fetched_item_{self.lm.parents}_{self.lm.children}'),
                        dot=Dot(),
                    ),
                    operator=AddAssign(),
                    value=Name(f'_add_links_to_{self.lm.child}'),
                ),
            ],
            leading_lines=[
                # Add an empty line before the next statement.
                EmptyLine(
                    indent=False,
                    whitespace=SimpleWhitespace(''),
                    newline=Newline(),
                ),
            ],
            trailing_whitespace=TrailingWhitespace(
                whitespace=SimpleWhitespace(''),
                newline=Newline(),
            ),
        )

        # Create the second SimpleStatementLine with the on_fetched_resource hook.
        on_fetched_resource_line = SimpleStatementLine(
            body=[
                AugAssign(
                    target=Attribute(
                        value=Name('app'),
                        attr=Name(f'on_fetched_resource_{self.lm.parents}_{self.lm.children}'),
                        dot=Dot(),
                    ),
                    operator=AddAssign(),
                    value=Name(f'_add_links_to_{self.lm.parents}_collection'),
                ),
            ],
            leading_lines=[],
            trailing_whitespace=TrailingWhitespace(
                whitespace=SimpleWhitespace(''),
                newline=Newline(),
            ),
        )

        # Create the third SimpleStatementLine with the on_post_POST hook.
        on_post_POST_line1 = SimpleStatementLine(
            body=[
                AugAssign(
                    target=Attribute(
                        value=Name('app'),
                        attr=Name(f'on_post_POST_{self.lm.parents}_{self.lm.children}'),
                        dot=Dot(),
                    ),
                    operator=AddAssign(),
                    value=Name('add_etag_header_to_post'),
                ),
            ],
            leading_lines=[],
            trailing_whitespace=TrailingWhitespace(
                whitespace=SimpleWhitespace(''),
                newline=Newline(),
            ),
        )

        # Create the third SimpleStatementLine with the on_post_POST hook.
        on_post_POST_line2 = SimpleStatementLine(
            body=[
                AugAssign(
                    target=Attribute(
                        value=Name('app'),
                        attr=Name(f'on_post_POST_{self.lm.parents}_{self.lm.children}'),
                        dot=Dot(),
                    ),
                    operator=AddAssign(),
                    value=Name(f'_post_{self.lm.children}'),
                ),
            ],
            leading_lines=[],
            trailing_whitespace=TrailingWhitespace(
                whitespace=SimpleWhitespace(''),
                newline=Newline(),
            ),
        )
        # Return the list of SimpleStatementLines.
        return [on_fetched_item_line, on_fetched_resource_line, on_post_POST_line1, on_post_POST_line2]
