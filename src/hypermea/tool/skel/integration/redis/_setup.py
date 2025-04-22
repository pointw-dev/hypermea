from libcst import *
from hypermea.tool import code_gen, install_packages
from hypermea.tool.code_gen.file_transformer import FileTransformer


class RedisInserter(FileTransformer):
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
                        value=Name('integration'),
                        dot=Dot(),
                        attr=Name('redis')
                    ),
                    names=[
                        ImportAlias(
                            name=Name('get_redis_client')
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
            value=Call(
                func=Name(value='get_redis_client',),
            ),
            keyword=Name(value='redis',),
            equal=AssignEqual(
                whitespace_before=SimpleWhitespace(
                    value='',
                ),
                whitespace_after=SimpleWhitespace(
                    value='',
                ),
            )
        )

        new_value = code_gen.get_new_param_list(addition, updated_node)

        return updated_node.with_changes(
            value=new_value
        )


def setup():
    RedisInserter().transform('hypermea_service.py', )
    install_packages(['redis'], 'redis integration')
