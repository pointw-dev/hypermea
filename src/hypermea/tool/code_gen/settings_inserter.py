from libcst import *
from .base_settings_inserter import BaseSettingsInserter
from hypermea.tool import code_gen


class SettingsInserter(BaseSettingsInserter):
    def __init__(self, module_name: str, class_name: str, tag: str = None):
        super().__init__(module_name, class_name, tag)

        self.registry_entry = self.get_dict_element()
        self.function_definition = self.get_function_def()
        self.assignment_statement_line = self.get_assignment_statement_line()


    def leave_Call(self, original_node, updated_node):
        if not original_node.func.value == 'load_ordered_env_files':
            return original_node

        new_args = self.insert_settings_class(updated_node) if self.module_name == 'settings' else self.insert_integration_class(updated_node)

        return updated_node.with_changes(
            args=new_args
        )

    def insert_settings_class(self, updated_node):
        elements = updated_node.args[0].value.elements
        new_elements = []
        for element in elements:
            if isinstance(element.comma, Comma) and isinstance(element.comma.whitespace_after, ParenthesizedWhitespace):
                element = element.with_changes(comma=Comma(
                    whitespace_after=SimpleWhitespace(
                        value=' ',
                    )))
                new_elements.append(element)
                new_elements.append(Element(value=Name(self.class_name), comma=code_gen.COMMA))
            else:
                new_elements.append(element)
        new_elements = tuple(new_elements)
        new_arg = updated_node.args[0].with_changes(
            value=updated_node.args[0].value.with_changes(
                elements=new_elements
            )
        )
        new_args = (new_arg,)
        return new_args

    def insert_integration_class(self, updated_node):
        elements = updated_node.args[0].value.elements
        last_element = elements[-1].with_changes(comma=Comma(
            whitespace_after=SimpleWhitespace(
                value=' ',
            )))
        new_element = Element(value=Name(self.class_name), comma=MaybeSentinel.DEFAULT)
        new_elements = tuple(elements[:-1] + (last_element, new_element))
        new_arg = updated_node.args[0].with_changes(
            value=updated_node.args[0].value.with_changes(
                elements=new_elements
            )
        )
        new_args = (new_arg,)
        return new_args

    def leave_Assign(self, original_node, updated_node):
        target_value = original_node.targets[0].target.value
        if not original_node.targets[0].target.value in ['__all__', '_registry']:
            return original_node

        if target_value == '__all__':
            new_elements = []
            for element in original_node.value.elements[:-1]:
                if isinstance(element.comma, Comma) and isinstance(element.comma.whitespace_after, ParenthesizedWhitespace):
                    new_elements.append(element.with_changes(comma=Comma()))
                    new_elements.append(Element(value=SimpleString(value=f"'get_{self.tag}'"),comma=code_gen.COMMA))
                else:
                    new_elements.append(element)
            new_elements.append(original_node.value.elements[-1].with_changes(comma=Comma()))
            new_elements.append(Element(value=SimpleString(value=f"'{self.tag}'"), comma=MaybeSentinel.DEFAULT))

            return updated_node.with_changes(
                value=original_node.value.with_changes(
                    elements=new_elements
                )
            )

        if target_value == '_registry':
            last_element = updated_node.value.elements[-1].with_changes(comma=Comma(
                whitespace_after=ParenthesizedWhitespace(
                    first_line=code_gen.TWNL,
                    last_line=SimpleWhitespace(
                        value='    ',
                    ),
                ),
            ))
            new_elements = tuple(updated_node.value.elements[:-1] + (last_element, self.registry_entry))

            return updated_node.with_changes(
                value=original_node.value.with_changes(
                    elements=new_elements
                )
            )

        return original_node


    def leave_Module(self, original_node, updated_node):
        """ Adds to the top of hypermea_service.py the following:
                from .hypermea import HypermeaSettings
                or
                from integration.mongo.settings import MongoSettings
        """
        new_body = self.insert_import_statement(updated_node)
        new_body = self.insert_function_definition(new_body)
        new_body = self.insert_assignment_statement(new_body)

        return updated_node.with_changes(
            body=new_body
        )

    def insert_assignment_statement(self, new_body):
        statements = []
        for node in new_body:
            if isinstance(node, SimpleStatementLine) and isinstance(node.body[0], Assign):
                if node.body[0].targets[0].target.value == '__all__':
                    statements.append(self.assignment_statement_line)
            statements.append(node)
        new_body = statements
        return new_body

    def insert_function_definition(self, new_body):
        statements = []
        inside_function_section = False
        for node in new_body:
            if isinstance(node, FunctionDef):
                inside_function_section = True

            if inside_function_section and not isinstance(node, FunctionDef):
                inside_function_section = False
                statements.append(self.function_definition)

            statements.append(node)
        new_body = statements
        return new_body

    def get_assignment_statement_line(self):
        return SimpleStatementLine(
            body=[
                Assign(
                    targets=[
                        AssignTarget(
                            target=Name(value=self.tag)
                        )
                    ],
                    value=Call(
                        func=Name(f'get_{self.tag}')
                    )
                )
            ],
            trailing_whitespace=code_gen.TWNL
        )

    def get_function_def(self):
        return FunctionDef(
            name=Name(value=f'get_{self.tag}'),
            params=Parameters(),
            body=SimpleStatementSuite(
                body=[
                    Return(
                        value=Subscript(
                            value=Name('_registry'),
                            slice=[
                                SubscriptElement(
                                    slice=Index(
                                        value=SimpleString(f"'{self.tag}'")
                                    )
                                )
                            ]
                        )
                    )
                ]
            )
        )

    def get_dict_element(self):
        return DictElement(
            key=SimpleString(value=f"'{self.tag}'"),
            value=Call(
                func=Name(value=self.class_name)
            ),
        )

