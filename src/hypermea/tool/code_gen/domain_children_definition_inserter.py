from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class DomainChildrenDefinitionInserter(FileTransformer):
    def __init__(self, link_manager):
        super().__init__()
        self.lm = link_manager

    def visit_SimpleStatementLine(self, node):
        if not isinstance(node.body[0], Assign):
            return False

        if not node.body[0].targets[0].target.value == 'SCHEMA':
            return False

        return True

    def leave_Assign(self, original_node, updated_node):
        new_elements = []
        for item in original_node.value.elements[:-1]:
            new_elements.append(item)
        new_elements.append(original_node.value.elements[-1].with_changes (comma=code_gen.COMMA))
        new_elements.append(self.make_parent_ref())

        members = Dict(elements=new_elements,
                lbrace=LeftCurlyBrace(
                    whitespace_after=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('    ')
                    )
                ),
                rbrace=RightCurlyBrace(
                    whitespace_before=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True
                    )
                )
            )

        return updated_node.with_changes (value=members)

    def make_parent_ref(self):
        """ Adds the following to domain/children.py's SCHEMA:
                '_parent_ref': {
                    'type': 'objectid',
                    'data_relation': {
                        'resource': 'parents',
                        'embeddable': True
                    }
                }
            or if parent is external:
                '_parent_external_id': {
                    'type': 'objectid'
                }
        """

        type_element = DictElement(
            key=SimpleString("'type'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=SimpleString("'objectid'"),
            comma=Comma(
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    indent=True,
                    last_line=SimpleWhitespace('        ')
                )
            )
        )

    # TODO: refactor the following...
        resource_element = DictElement(
            key=SimpleString("'resource'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=SimpleString(f"'{self.lm.parents}'"),
            comma=Comma(
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    indent=True,
                    last_line=SimpleWhitespace('            ')
                )
            ),
        )

        embeddable_element = DictElement(
            key=SimpleString("'embeddable'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=Name('True')
        )

        gateway_element = DictElement(
            key=SimpleString("'rel'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=SimpleString(f"'{self.lm.parents}'"),
            comma=Comma(
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    indent=True,
                    last_line=SimpleWhitespace('            ')
                )
            ),
        )


        data_relation_element = DictElement(
            key=SimpleString("'data_relation'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=Dict(
                elements=[
                    resource_element,
                    embeddable_element
                ],
                lbrace=LeftCurlyBrace(
                    whitespace_after=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('            ')
                    ),
                ),
                rbrace=RightCurlyBrace(
                    whitespace_before=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('        ')
                    )
                )
            )
        )

        external_relation_element = DictElement(
            key=SimpleString("'external_relation'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=Dict(
                elements=[
                    gateway_element,
                    embeddable_element
                ],
                lbrace=LeftCurlyBrace(
                    whitespace_after=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('            ')
                    ),
                ),
                rbrace=RightCurlyBrace(
                    whitespace_before=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('        ')
                    )
                )
            )
        )


        elements =[type_element]
        if self.lm.external_parent:
            elements.append(external_relation_element)
        else:
            elements.append(data_relation_element)

        return DictElement(
            key=SimpleString(f"'{self.lm.parent_ref}'"),
            value=Dict(
                elements=elements,
                lbrace=LeftCurlyBrace(
                    whitespace_after=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('        ')
                    )
                ),
                rbrace=RightCurlyBrace(
                    whitespace_before=ParenthesizedWhitespace(
                        first_line=code_gen.TWNL,
                        indent=True,
                        last_line=SimpleWhitespace('    '),
                    )
                )
            ),
            whitespace_after_colon=SimpleWhitespace(' ')
        )
