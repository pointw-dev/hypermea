import itertools
from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class DomainDefinitionInserter(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_Module(self, original_node, updated_node):
        """ Adds the following to the top of domain/__init__.py:
               from . import resource
        """
        addition = SimpleStatementLine(
            body=[
                ImportFrom(
                    module=None,
                    names=[
                        ImportAlias(
                            name=Name(f'{self.resource}')
                        ),
                    ],
                    relative=[
                        Dot(),
                    ],
                    whitespace_after_from=SimpleWhitespace(' '),
                    whitespace_before_import=SimpleWhitespace(' '),
                    whitespace_after_import=SimpleWhitespace(' ')
                )
            ],
            trailing_whitespace=code_gen.TWNL
        )

        new_body = code_gen.insert_import(updated_node.body, addition)

        return updated_node.with_changes(
            body=new_body
        )

    def visit_SimpleStatementLine(self, node):
        if not isinstance(node.body[0], Assign):
            return False

        if not node.body[0].targets[0].target.value == 'DOMAIN_DEFINITIONS':
            return False

        return True

    def leave_Assign(self, original_node, updated_node):
        # TODO: refactor with domain_relations_inserter
        # TODO: remove trailing comma after last element
        new_elements = []
        if original_node.value.elements:
            for item in original_node.value.elements[:-1]:
                new_elements.append(item)
            new_elements.append(original_node.value.elements[-1].with_changes (comma=code_gen.COMMA))
        new_elements.append(self.make_domain_defintion())

        definitions = Dict(
            elements=new_elements,
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
                    indent=True,
                )
            )
        )

        return updated_node.with_changes(value=definitions)

    def make_domain_defintion(self):
        """ Adds the following to domain/__init_.py's DOMAIN_DEFINITIONS:
            'resource': resource.DEFINITION,
        """
        return DictElement(
            key=SimpleString(f"'{self.resource}'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=Attribute(
                value=Name(f'{self.resource}'),
                dot=Dot(),
                attr=Name('DEFINITION'),
            ),
            comma=Comma(
                whitespace_before=SimpleWhitespace(
                    value='',
                ),
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    indent=True,
                    last_line=SimpleWhitespace('    ')
                )
            )
        )
