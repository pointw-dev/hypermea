from libcst import *
from .file_transformer import FileTransformer
from hypermea.tool import code_gen


class AuthorizationInserter(FileTransformer):
    def __init__(self):
        super().__init__()

    def leave_Module(self, original_node, updated_node):
        """ Adds to the top of hypermea_service.py the following:
                from auth.authorization import HypermeaAuthorization
        """

        addition = SimpleStatementLine(
            body=[
                ImportFrom(
                    module=Attribute(
                        value=Name('auth'),
                        dot=Dot(),
                        attr=Name('authorization')
                    ),
                    names=[
                        ImportAlias(
                            name=Name('HypermeaAuthorization')
                        )
                    ],
                    whitespace_after_from=SimpleWhitespace(' '),
                    whitespace_before_import=SimpleWhitespace(' '),
                    whitespace_after_import=SimpleWhitespace(' ')
                )
            ])

        new_body = code_gen.insert_import(updated_node.body, addition)

        return updated_node.with_changes(
            body=new_body
        )

    def visit_SimpleStatementLine(self, node):
        return code_gen.is_app_assignment(node)

    def leave_Assign(self, original_node, updated_node):
        """ Adds the following kwarg to hypermea_service.py:HypermeaService:__init__() self._app = Eve(...) assignment:
                auth=HypermeaAuthorization
        """

        addition = Arg(
            value=Name('HypermeaAuthorization'),
            equal=AssignEqual(
                whitespace_before=SimpleWhitespace(''),
                whitespace_after=SimpleWhitespace('')
            ),
            keyword=Name('auth')
        )
        
        new_value = code_gen.get_new_param_list(addition, updated_node)

        return updated_node.with_changes(
            value=new_value
        )
