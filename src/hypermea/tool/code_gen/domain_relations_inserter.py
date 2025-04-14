import os

from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class DomainRelationsInserter(FileTransformer):
    def __init__(self, adder):
        super().__init__()
        self.adder = adder

    def transform(self, filename):
        super().transform(filename)

    def leave_Assign(self, original_node, updated_node):
        if not original_node.targets[0].target.value == 'RELATION_REGISTRY':
            return original_node

        new_elements = []
        if original_node.value.elements:
            for item in original_node.value.elements[:-1]:
                new_elements.append(item)
            new_elements.append(original_node.value.elements[-1].with_changes (comma=code_gen.COMMA))

        new_elements.append(self.make_domain_relation())
        new_elements = tuple(new_elements)

        return updated_node.with_changes(
            value=updated_node.value.with_changes(
                elements=new_elements,
                lbracket=LeftSquareBracket(
                    whitespace_after=ParenthesizedWhitespace(
                        last_line=SimpleWhitespace(value='    ')
                    )
                ),
                rbracket=RightSquareBracket(
                    whitespace_before=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL
                    )
                )
            )
        )

    def make_domain_relation(self):
        return Element(
            value=Call(
                func=Name(value='Relation',),
                args=[
                    Arg(
                        value=SimpleString(value=f'"{self.adder.parent}"',),
                        keyword=Name(value='parent',),
                        equal=AssignEqual(),
                        comma=Comma(),
                    ),
                    Arg(
                        value=SimpleString(value=f"'{self.adder.child}'",),
                        keyword=Name(value='child',),
                        equal=AssignEqual(),
                        comma=MaybeSentinel.DEFAULT,
                    ),
                ],
            )
        )
