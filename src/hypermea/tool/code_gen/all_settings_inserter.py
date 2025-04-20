from typing import Union

from libcst import *
from .base_settings_inserter import BaseSettingsInserter
from hypermea.tool import code_gen


class AllSettingsInserter(BaseSettingsInserter):
    def __init__(self, module_name: str, class_name: str, tag: str = None):
        super().__init__(module_name, class_name, tag)

    def leave_Module(self, original_node, updated_node):
        new_body = self.insert_import_statement(updated_node)

        return updated_node.with_changes(
            body=new_body
        )

    def leave_ImportFrom(self, original_node, updated_node):
        if not original_node.module is None and not original_node.names[0].name.value == '_registry':
            return updated_node

        new_names = tuple(
            original_node.names[:-1] +
            (
                updated_node.names[-1].with_changes(comma=Comma(whitespace_after=SimpleWhitespace(value=' ',))),
                ImportAlias(
                    name=Name(
                        value=f'get_{self.tag}',
                    ),
                    comma=MaybeSentinel.DEFAULT,
                )
            )
        )

        return updated_node.with_changes(
            names=new_names
        )


    def leave_ClassDef(self, original_node, updated_node):
        if not original_node.name.value == 'AllSettings':
            return updated_node

        new_body = tuple(
            original_node.body.body +
            (
                SimpleStatementLine(
                    body=[
                        AnnAssign(
                            target=Name(value=f'{self.tag}',),
                            annotation=Annotation(
                                annotation=Name(value=f'{self.class_name}',),
                                whitespace_after_indicator=SimpleWhitespace(value=' ',),
                            ),
                            equal=MaybeSentinel.DEFAULT,
                            semicolon=MaybeSentinel.DEFAULT,
                        ),
                    ],
                    trailing_whitespace=code_gen.TWNL,
                ),
            )
        )
        return updated_node.with_changes(
            body=updated_node.body.with_changes(
                body=new_body
            )
        )

    def leave_FunctionDef(self, original_node, updated_node):
        if not original_node.name.value in ['get_settings', 'build_settings']:
            return updated_node
        fn = updated_node.name.value
        rtn = updated_node
        if fn == 'get_settings':
            rtn = self.add_to_get_settings(updated_node)
        elif fn == 'build_settings':
            rtn = self.add_to_build_settings(updated_node)

        return rtn

    def leave_Assign(self, original_node, updated_node):
        if not isinstance(updated_node.targets[0].target.value, str) or not updated_node.targets[0].target.value == 'settings_models':
            return updated_node

        new_elements = tuple(
            updated_node.value.elements[:-1] +
            (
                updated_node.value.elements[-1].with_changes(
                    comma=Comma(
                        whitespace_before=SimpleWhitespace(value='',),
                        whitespace_after=ParenthesizedWhitespace(
                            first_line=TrailingWhitespace(
                                whitespace=SimpleWhitespace(
                                    value='',
                                ),
                                comment=None,
                                newline=Newline(
                                    value=None,
                                ),
                            ),
                            empty_lines=[],
                            indent=True,
                            last_line=SimpleWhitespace(
                                value='    ',
                            ),
                        ),
                    )
                ),
                Element(
                    value=Tuple(
                        elements=[
                            Element(
                                value=SimpleString(value=f'"{self.tag}"',),
                                comma=Comma(
                                    whitespace_before=SimpleWhitespace(value='',),
                                    whitespace_after=SimpleWhitespace(value=' ',),
                                ),
                            ),
                            Element(
                                value=Call(
                                    func=Name(value=f'get_{self.tag}',),
                                    whitespace_after_func=SimpleWhitespace(value='',),
                                    whitespace_before_args=SimpleWhitespace(value='',),
                                ),
                                comma=MaybeSentinel.DEFAULT,
                            ),
                        ],
                        lpar=[
                            LeftParen(
                                whitespace_after=SimpleWhitespace(
                                    value='',
                                ),
                            ),
                        ],
                        rpar=[
                            RightParen(
                                whitespace_before=SimpleWhitespace(
                                    value='',
                                ),
                            ),
                        ],
                    ),
                    comma=MaybeSentinel.DEFAULT,
                )
            )
        )
        new_node = updated_node.with_changes(
            value=updated_node.value.with_changes(
                elements=new_elements,
            )
        )
        return new_node

    def add_to_get_settings(self, updated_node):
        old_call = updated_node.body.body[0].body[0].value  # This is a Call node
        new_args = tuple(
            old_call.args[:-1] +
            (
                old_call.args[-1].with_changes(
                    comma=Comma(
                        whitespace_before=SimpleWhitespace(value='',),
                        whitespace_after=ParenthesizedWhitespace(
                            first_line=TrailingWhitespace(
                                whitespace=SimpleWhitespace(value='',),
                            ),
                            indent=True,
                            last_line=SimpleWhitespace(value='    ',),
                        ),
                    ),
                    star='',
                    whitespace_after_star=SimpleWhitespace(value='', ),
                    whitespace_after_arg=SimpleWhitespace(value='', ),
                ),
                Arg(
                    value=Call(
                        func=Name(value=f'get_{self.tag}'),
                    ),
                    keyword=Name(value=self.tag),
                    equal=AssignEqual(
                        whitespace_before=SimpleWhitespace(value=''),
                        whitespace_after=SimpleWhitespace(value=''),
                    ),
                    comma=MaybeSentinel.DEFAULT,
                    whitespace_after_arg=ParenthesizedWhitespace(
                        first_line=TrailingWhitespace(
                            whitespace=SimpleWhitespace(
                                value='',
                            ),
                        ),
                        indent=True,
                    ),
                ),
            )
        )
        new_call = old_call.with_changes(args=new_args)
        new_expr_stmt = updated_node.body.body[0].body[0].with_changes(value=new_call)
        new_inner_body = updated_node.body.body[0].with_changes(body=[new_expr_stmt])
        new_outer_body = updated_node.body.with_changes(body=[new_inner_body])
        rtn = updated_node.with_changes(body=new_outer_body)
        return rtn

    def add_to_build_settings(self, updated_node):
        new_params = self.get_build_settings_params(updated_node)

        new_args = tuple(
            updated_node.body.body[1].body[0].value.args[:-1] +
            (
                updated_node.body.body[1].body[0].value.args[-1].with_changes(
                    comma=Comma(
                        whitespace_before=SimpleWhitespace(value='',),
                        whitespace_after=ParenthesizedWhitespace(
                            first_line=TrailingWhitespace(
                                whitespace=SimpleWhitespace(value='',),
                                comment=None,
                                newline=Newline(value=None,),
                            ),
                            empty_lines=[],
                            indent=True,
                            last_line=SimpleWhitespace(value='    ',),
                        ),
                    ),
                    star='',
                    whitespace_after_star=SimpleWhitespace(value='',),
                    whitespace_after_arg=SimpleWhitespace(value='',)
                ),
                Arg(
                    value=BooleanOperation(
                        left=Name(value=self.tag,),
                        operator=Or(
                            whitespace_before=SimpleWhitespace(value=' ',),
                            whitespace_after=SimpleWhitespace(value=' ',),
                        ),
                        right=Attribute(
                            value=Name(value='defaults',),
                            attr=Name(value=self.tag,),
                            dot=Dot(),
                        ),
                    ),
                    keyword=Name(value=self.tag,),
                    equal=AssignEqual(
                        whitespace_before=SimpleWhitespace(value='',),
                        whitespace_after=SimpleWhitespace(value='',),
                    ),
                    comma=MaybeSentinel.DEFAULT,
                    whitespace_after_star=SimpleWhitespace(value='',),
                    whitespace_after_arg=ParenthesizedWhitespace(
                        first_line=TrailingWhitespace(
                            whitespace=SimpleWhitespace(value='',),
                            comment=None,
                            newline=Newline(value=None,),
                        ),
                        empty_lines=[],
                        indent=True,
                        last_line=SimpleWhitespace(value='',),
                    ),
                )
            )
        )

        old_call = updated_node.body.body[1].body[0].value
        new_call = old_call.with_changes(args=new_args)
        old_stmt = updated_node.body.body[1].body[0]
        new_stmt = old_stmt.with_changes(value=new_call)
        old_inner_body = updated_node.body.body[1]
        new_inner_body = old_inner_body.with_changes(body=[new_stmt])
        new_body = updated_node.body.with_changes(
            body=[
                updated_node.body.body[0],  # preserve first item
                new_inner_body  # replace second item
            ]
        )

        return updated_node.with_changes(
            params=updated_node.params.with_changes(
                params=new_params
            ),
            body=new_body,
        )

    def get_build_settings_params(self, updated_node):
        new_params = tuple(
            updated_node.params.params[:-1] +
            (
                updated_node.params.params[-1].with_changes(
                    comma=Comma(
                        whitespace_before=SimpleWhitespace(value='', ),
                        whitespace_after=ParenthesizedWhitespace(
                            first_line=TrailingWhitespace(
                                whitespace=SimpleWhitespace(value='', ),
                                comment=None,
                                newline=Newline(value=None)
                            ),
                            indent=True,
                            last_line=SimpleWhitespace(value='    ', ),
                        ),
                    ),
                    star='',
                    whitespace_after_star=SimpleWhitespace(value='', ),
                    whitespace_after_param=SimpleWhitespace(value='', ),
                ),
                Param(
                    name=Name(value=self.tag, ),
                    annotation=Annotation(
                        annotation=Name(value=self.class_name, ),
                        whitespace_before_indicator=SimpleWhitespace(value='', ),
                        whitespace_after_indicator=SimpleWhitespace(value=' ', ),
                    ),
                    equal=AssignEqual(
                        whitespace_before=SimpleWhitespace(value=' ', ),
                        whitespace_after=SimpleWhitespace(value=' ', ),
                    ),
                    default=Name(value='None', ),
                    comma=MaybeSentinel.DEFAULT,
                    whitespace_after_star=SimpleWhitespace(value='', ),
                    whitespace_after_param=ParenthesizedWhitespace(
                        first_line=TrailingWhitespace(
                            whitespace=SimpleWhitespace(value='', ),
                            newline=Newline(
                                value=None,
                            )
                        ),
                        indent=True,
                        last_line=SimpleWhitespace(
                            value='',
                        ),
                    ),
                )
            )
        )
        return new_params
