import os

from libcst import *

from hypermea.tool import code_gen
from .file_transformer import FileTransformer


class DomainRelationsInserter(FileTransformer):
    def __init__(self, link_manager):
        super().__init__()
        self.lm = link_manager

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
        parent_arg = self.get_arg('parent')
        child_arg = self.get_arg('child')

        relation = Element(
            value=Call(
                func=Name(value='Relation',),
                args=[parent_arg, child_arg],
            )
        )

        return relation

    def get_arg(self, which):
        rel = self.lm.relation.parent if which == 'parent' else self.lm.relation.child

        if rel.external:
            parent_arg = Arg(
                value=Call(
                    func=Name(value='external', ),
                    args=[
                        Arg(
                            value=SimpleString(value=f"'{rel}'", ),
                            keyword=None,
                            equal=MaybeSentinel.DEFAULT,
                            comma=MaybeSentinel.DEFAULT,
                            star='',
                            whitespace_after_star=SimpleWhitespace(value='', ),
                            whitespace_after_arg=SimpleWhitespace(value='', ),
                        ),
                    ],
                ),
                keyword=Name(value=f'{which}', ),
                equal=AssignEqual(
                    whitespace_before=SimpleWhitespace(value='', ),
                    whitespace_after=SimpleWhitespace(value='', ),
                ),
                comma=MaybeSentinel.DEFAULT if which == 'child' else Comma(whitespace_after=SimpleWhitespace(value=' ', ), ),
            )
        else:
            parent_arg = Arg(
                value=SimpleString(value=f"'{rel}'", ),
                keyword=Name(value=f'{which}', ),
                equal=AssignEqual(
                    whitespace_before=SimpleWhitespace(value='', ),
                    whitespace_after=SimpleWhitespace(value='', ),
                ),
                comma=MaybeSentinel.DEFAULT if which == 'child' else Comma(whitespace_after=SimpleWhitespace(value=' ', ), ),
            )
        return parent_arg
