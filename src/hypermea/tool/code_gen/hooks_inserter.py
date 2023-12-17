import itertools
from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class HooksInserter(FileTransformer):
    def __init__(self, resource):
        super().__init__()
        self.resource = resource

    def leave_Module(self, original_node, updated_node):
        """ Adds the following to the top of hooks/__init__.py
                import hooks.resource
        """

        addition = SimpleStatementLine(
            body=[
                Import(
                    names=[ImportAlias(name=Attribute(Name('hooks'), attr=Name(f'{self.resource}')))],
                    whitespace_after_import=SimpleWhitespace(' ')
                )
            ],
            trailing_whitespace=code_gen.TWNL
        )

        new_body = code_gen.insert_import(updated_node.body, addition)

        return updated_node.with_changes(
            body=new_body
        )

    def leave_FunctionDef(self, original_node, updated_node):
        """ Adds the following to hooks/__init__.py:add_hooks():
                hooks.resource.add_hooks(app)
        """
        if not original_node.name.value == 'add_hooks':
            return original_node

        addition = SimpleStatementLine(
            body=[
                Expr(
                    value=Call(
                        func=Attribute(
                            value=Attribute(
                                value=Name('hooks'),
                                dot=Dot(),
                                attr=Name(f'{self.resource}'),
                            ),
                            dot=Dot(),
                            attr=Name('add_hooks'),
                        ),
                        args=[Arg(Name('app'))]
                    )
                )
            ],
            trailing_whitespace=code_gen.TWNL
        )

        new_body = []
        for item in itertools.chain(updated_node.body.body, [addition]):  # TODO: if addition is first, prepend with newline
            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
