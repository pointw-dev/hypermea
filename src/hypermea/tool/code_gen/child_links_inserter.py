from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class ChildLinksInserter(FileTransformer):
    def __init__(self, adder):
        super().__init__()
        self.adder = adder

    def leave_FunctionDef(self, original_node, updated_node):
        if not self.adder.relation.parent.external or not original_node.name.value == '_add_external_parent_links':
            return original_node

        new_body = []
        for item in original_node.body.body:
            new_body.append(item)

        new_body.append(self.make_parent_link())

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )

    def make_parent_link(self):
        """ This adds the following to hooks.child:_add_external_parent_links()
                if '_parent_ref' in child:
                    child['_links']['parent'] = {  # not literally 'parent' here, rather the name of the parent resource
                        'href': '{get_href_from_gateway('parents')"]}/{child[_parent_ref]}",
                        'title': 'parent_children'
                    }

        """

        if self.adder.relation.parent.external:
            href = FormattedString(
                parts=[
                    FormattedStringExpression(
                        expression=Call(
                            func=Name('get_href_from_gateway'),
                            args=[
                                Arg(SimpleString(f"'{self.adder.relation.parent}'"))
                            ]
                        )
                    ),
                    FormattedStringText('/'),
                    FormattedStringExpression(
                        expression=Subscript(
                            value=Name(str(self.adder.relation.child)),
                            slice=[
                                SubscriptElement(
                                    slice=Index(SimpleString(f"'_{self.adder.relation.parent}_ref'"))
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
                resource=str(self.adder.relation.child),
                rel=str(self.adder.relation.parent),
                href=href,
            )

            return If(
                test=Comparison(
                    left=SimpleString(f"'_{self.adder.relation.parent}_ref'"),
                    comparisons=[
                        ComparisonTarget(
                            operator=In(
                                whitespace_before=SimpleWhitespace(' '),
                                whitespace_after=SimpleWhitespace(' ')
                            ),
                            comparator=Name(str(self.adder.relation.child))
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

        condition = Call(
            func=Attribute(
                value=Name(f'{self.adder.relation.child}'),
                attr=Name('get'),
                dot=Dot()
            ),
            args=[
                Arg(SimpleString(f"'{self.adder.relation.parent}_ref'"))
            ]
        )

        if_block = IndentedBlock(
            body=[
                code_gen.get_link_statement_line(
                    resource=str(self.adder.relation.child),
                    rel='parent',
                    href=[
                        FormattedStringText(f'/{self.adder.parents}/'),
                        FormattedStringExpression(
                            expression=Subscript(
                                value=Name(f'{self.adder.relation.child}'),
                                slice=[
                                    SubscriptElement(
                                        slice=Index(SimpleString(f'"{self.adder.parent_ref}"'))
                                    ),
                                ],
                                lbracket=LeftSquareBracket(),
                                rbracket=RightSquareBracket()
                            ),
                        )
                    ]
                ),
                code_gen.get_link_statement_line(
                    resource=str(self.adder.relation.child),
                    rel='collection',
                    href=[
                        FormattedStringText(f'/{self.adder.parents}/'),
                        FormattedStringExpression(
                            expression=Subscript(
                                value=Name(f'{self.adder.relation.child}'),
                                slice=[
                                    SubscriptElement(
                                        slice=Index(SimpleString(f'"{self.adder.parent_ref}"'))
                                    ),
                                ],
                                lbracket=LeftSquareBracket(),
                                rbracket=RightSquareBracket()
                            )
                        ),
                        FormattedStringText(f'/{self.adder.children}')
                    ]
                )
            ],
            header=code_gen.TWNL
        )

        else_block = Else(
            body=IndentedBlock(
                body=[
                    code_gen.get_link_statement_line(
                        resource=str(self.adder.relation.child),
                        rel='parent',
                        href=[FormattedStringText('/')]
                    ),
                    code_gen.get_link_statement_line(
                        resource=str(self.adder.relation.child),
                        rel='collection',
                        href=[FormattedStringText(f'/{self.adder.children}')]
                    )
                ],
                header=code_gen.TWNL
            )
        )

        return If(
            test=condition,
            body=if_block,
            orelse=else_block,
            whitespace_before_test=SimpleWhitespace(' ')
        )
