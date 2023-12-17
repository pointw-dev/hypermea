import itertools
from libcst import *
import libcst.matchers as m
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class AffordanceRouteInserter(FileTransformer):
    def __init__(self, affordance):
        super().__init__()
        self.affordance = affordance

    def leave_Module(self, original_node, updated_node):
        """ Adds the following to the top of hooks/resource.py
                import affordances
        """
        if m.findall(original_node, m.ImportAlias(m.Name(value="affordances"))):
            return updated_node

        addition = SimpleStatementLine(
            body=[
                Import(
                    names=[ImportAlias(name=Name('affordances'))],
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
        """ Adds the following to hooks/resource.py:add_hooks():
                affordances.folder.add_affordance(app)
        """
        method_prefix = Attribute(
            value=Attribute(
                value=Name('affordances'),
                dot=Dot(),
                attr=Name(self.affordance.folder)
            ),
            dot=Dot(),
            attr=Name(self.affordance.identifier),
        ) if self.affordance.folder else Attribute(
            value=Name('affordances'),
            dot=Dot(),
            attr=Name(self.affordance.identifier)
        )
        additions = {
            'add_hooks': SimpleStatementLine(
                body=[
                    Expr(
                        value=Call(
                            func=Attribute(
                                value=method_prefix,
                                dot=Dot(),
                                attr=Name('add_affordance'),
                            ),
                            args=[Arg(Name('app'))]
                        )
                    )
                ],
                trailing_whitespace=code_gen.TWNL
            )
        }

        if original_node.name.value not in additions:
            return original_node

        new_body = []

        for item in itertools.chain(updated_node.body.body, [additions[original_node.name.value]]):
            new_body.append(item)

        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )
