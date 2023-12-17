from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class DomainRelationsInserter(FileTransformer):
    def __init__(self, adder):
        super().__init__()
        self.adder = adder

    def visit_SimpleStatementLine(self, node):
        if not isinstance(node.body[0], Assign):
            return False

        if not node.body[0].targets[0].target.value == 'DOMAIN_RELATIONS':
            return False

        return True

    def leave_Assign(self, original_node, updated_node):
        new_elements = []
        if original_node.value.elements:
            for item in original_node.value.elements[:-1]:
                new_elements.append(item)
            new_elements.append(original_node.value.elements[-1].with_changes (comma=code_gen.COMMA))
        new_elements.append(self.make_domain_relation())

        relations = Dict(
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

        return updated_node.with_changes(value=relations)

    @staticmethod
    def get_dict_element(key, value, with_comma=False):
        kwargs = {
            'key': SimpleString(f"'{key}'"),
            'whitespace_after_colon': SimpleWhitespace(' '),
            'value': value
        }
        if with_comma:
            kwargs['comma'] = Comma(
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    indent=True,
                    last_line=SimpleWhitespace('        ')
                )
            )
        return DictElement(**kwargs)

    def make_domain_relation(self):
        """ Adds the following to domain/__init__.py's DOMAIN_RELATIONS:
                'parents_children': {
                    'schema': children.SCHEMA,
                    'url': 'parents/<regex("[a-f0-9]{24}"):_parent_ref>/children',
                    'resource_title': 'children',
                    'datasource': {'source': 'children'}
                }
            or if remote parent
                'parents_children': {
                    'schema': children.SCHEMA,
                    'url': 'children/parent/<regex("[a-f0-9]{24}"):_parent_ref>',
                    'resource_title': 'children',
                    'datasource': {'source': 'children'}
                }

        """

        return DictElement(
            key=SimpleString(f"'{self.adder.parents}_{self.adder.children}'"),
            whitespace_after_colon=SimpleWhitespace(' '),
            value=Dict(
                elements=[
                    self.get_dict_element(
                        key='schema',
                        value=Attribute(
                            value=Name(f'{self.adder.children}'),
                            dot=Dot(),
                            attr=Name('SCHEMA')
                        ),
                        with_comma=True
                    ),
                    self.get_dict_element(
                        key='url',
                        value=FormattedString(
                            parts=[
                                FormattedStringText(f'{self.adder.children}/{self.adder.parent}/<regex("'),
                                FormattedStringExpression(expression=Name('OBJECT_ID_REGEX')),
                                FormattedStringText(f'"):{self.adder.parent_ref}>')
                            ],
                            start="f'",
                            end="'"
                        ) if self.adder.remote_parent else FormattedString(
                            parts=[
                                FormattedStringText(f'{self.adder.parents}/<regex("'),
                                FormattedStringExpression(expression=Name('OBJECT_ID_REGEX')),
                                FormattedStringText(f'"):{self.adder.parent_ref}>/{self.adder.children}')
                            ],
                            start="f'",
                            end="'"
                        ),
                        with_comma=True
                    ),
                    self.get_dict_element(
                        key='resource_title',
                        value=SimpleString(f"'{self.adder.children}'"),
                        with_comma=True
                    ),
                    self.get_dict_element(
                        key='datasource',
                        value=Dict(
                            elements=[
                                self.get_dict_element(
                                    key='source',
                                    value=SimpleString(f"'{self.adder.children}'")
                                )
                            ],
                            lbrace=LeftCurlyBrace(),
                            rbrace=RightCurlyBrace()
                        )
                    )
                ],
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
                        last_line=SimpleWhitespace('    ')
                    )
                )
            )
        )
