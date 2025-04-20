"""
Abstract base class for settings/all_settings inserters
"""

from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class BaseSettingsInserter(FileTransformer):
    def __init__(self, module_name: str, class_name: str, tag: str = None):
        super().__init__()
        self.module_name = module_name
        self.class_name = class_name  # e.g., 'RedisSettings'
        self.tag = tag if tag else class_name.replace("Settings", "").lower()  # e.g., 'redis'


    def insert_import_statement(self, updated_node):
        """ Adds to the following to the imports:
                from .hypermea import HypermeaSettings
                or
                from integration.mongo.settings import MongoSettings
        """
        import_statement = self.get_import_statement()
        if self.module_name != 'settings':
            new_body = code_gen.insert_import(updated_node.body, import_statement)
        else:
            before_statements = []
            after_statements = []

            before = True
            count = 0
            for statement in updated_node.body:
                if before and isinstance(statement.body, tuple) and isinstance(statement.body[0], ImportFrom):
                    if not statement.body[0].module is None and isinstance(statement.body[0].module.value, Attribute):
                        if statement.body[0].module.value.value.value == 'integration':
                            before = False
                            before_statements.append(import_statement)

                if before:
                    before_statements.append(statement)
                else:
                    after_statements.append(statement)
                count += 1

            new_body = [*before_statements, *after_statements]
        return new_body


    def get_import_statement(self):
        if self.module_name == 'settings':
            module = ImportFrom(
                module=Name(
                    value=self.tag
                ),
                names=[
                    ImportAlias(
                        name=Name(
                            value=self.class_name
                        )
                    )
                ],
                relative=[
                    Dot()
                ],
                whitespace_after_from=SimpleWhitespace(' '),
                whitespace_before_import=SimpleWhitespace(' '),
                whitespace_after_import=SimpleWhitespace(' ')
            )
        else:
            module = ImportFrom(
                module=Attribute(
                    value=Attribute(
                        value=Name(self.module_name),
                        attr=Name(value=self.tag),
                        dot=Dot()
                    ),
                    attr=Name(
                        value='settings'
                    ),
                    dot=Dot()
                ),
                names=[
                    ImportAlias(
                        name=Name(
                            value=self.class_name
                        )
                    )
                ]
            )
        addition = SimpleStatementLine(
            body=[module]
        )
        return addition

