import itertools
from libcst import *
from .domain_definition_inserter import DomainDefinitionInserter
from .hooks_inserter import HooksInserter
from .authorization_inserter import AuthorizationInserter
from .validation_inserter import ValidationInserter
from .child_links_inserter import ChildLinksInserter
from .parent_links_inserter import ParentLinksInserter
from .domain_children_definition_inserter import DomainChildrenDefinitionInserter
from .domain_relations_inserter import DomainRelationsInserter
from .affordance_inserter import  AffordanceInserter
from .domain_resource_remover import DomainResourceRemover
from .domain_relations_remover import DomainRelationsRemover
from .hooks_remover import HooksRemover
from .parent_reference_remover import ParentReferenceRemover
from .child_links_remover import ChildLinksRemover
from .affordance_detacher import AffordanceDetacher
from .affordance_remover import AffordanceRemover
from .affordance_import_remover import AffordanceImportRemover


TWNL = TrailingWhitespace(newline=Newline())

COMMA = Comma(
    whitespace_after=ParenthesizedWhitespace(
        first_line=TWNL,
        indent=True,
        last_line=SimpleWhitespace('    ')
    )
)


def insert_import(original_body, addition):
    rtn = []
    state = 'on-top'
    for item in original_body:
        if state == 'on-top':
            if not hasattr(item, 'body') \
                    or not hasattr(item.body, '__iter__') \
                    or type(item.body[0]).__name__ not in ['Import', 'ImportFrom', 'Expr']:
                state = 'in-position'

        if state == 'in-position':
            rtn.append(addition)  # TODO: if no other appends before, add newline after here
            state = 'on-bottom'

        rtn.append(item)

    return rtn


def get_link_statement_line(resource, rel, href, title):
    """ Creates the following
            resource['_links']['rel'] = {
                'href': 'href',
                'title': 'title'
            }
        where href is
            either a CST object that resolves to a quoted string
                e.g. SimpleString("'https://example.com'"
            or an array to insert into the parts of a FormattedString, to build a href on base_url
                e.g. [FormattedStringText(f'/{self.adder.children}')]
                    or the BinaryOperator return value of parent_links_inserter:_get_href_value()
    """

    if isinstance(href, list):
        value = FormattedString(
            start="f'",
            parts=[
                FormattedStringExpression(expression=Name('base_url')),
                *href
            ],
            end="'"
        )
    else:
        value = href

    href_element = DictElement(
        key=SimpleString("'href'"),
        value=value,
        comma=Comma(
            whitespace_after=ParenthesizedWhitespace(
                first_line=TrailingWhitespace(
                    newline=Newline(),
                ),
                indent=True,
                last_line=SimpleWhitespace('    ')  # four spaces
            )
        )
    )

    # Create the dictionary element with the 'title' key and simple string value.
    title_element = DictElement(
        key=SimpleString("'title'"),
        value=SimpleString(f"'{title}'")
    )

    # Create the dictionary with the above elements and left and right braces.
    link_dict = Dict(
        elements=[
            href_element,
            title_element
        ],
        lbrace=LeftCurlyBrace(
            whitespace_after=ParenthesizedWhitespace(
                first_line=TrailingWhitespace(
                    whitespace=SimpleWhitespace(''),
                    newline=Newline(),
                ),
                indent=True,
                last_line=SimpleWhitespace('    ')
            ),
        ),
        rbrace=RightCurlyBrace(
            whitespace_before=ParenthesizedWhitespace(
                first_line=TrailingWhitespace(
                    whitespace=SimpleWhitespace(''),
                    newline=Newline()
                ),
                indent=True
            )
        )
    )

    # Create the assignment statement with the 'links' subscript target and link_dict value.
    assign_statement = Assign(
        value=link_dict,
        targets=[
            AssignTarget(
                target=Subscript(
                    value=Subscript(
                        value=Name(resource),
                        slice=[SubscriptElement(slice=Index(SimpleString("'_links'")))]
                    ),
                    slice=[SubscriptElement(slice=Index(SimpleString(f"'{rel}'")))],
                    lbracket=LeftSquareBracket(),
                    rbracket=RightSquareBracket()
                ),
                whitespace_before_equal=SimpleWhitespace(' '),
                whitespace_after_equal=SimpleWhitespace(' ')
            )
        ]
    )

    return SimpleStatementLine(
        body=[
            assign_statement
        ],
        trailing_whitespace=TWNL
    )


def get_new_param_list(addition, updated_node):
    comma = Comma(whitespace_after=SimpleWhitespace(' '))

    new_args = []

    last_arg = updated_node.value.args[-1].with_changes(comma=comma)

    for item in itertools.chain(updated_node.value.args[0:-1], [last_arg, addition]):
        new_args.append(item)

    new_value = updated_node.value.with_changes(args=new_args)

    return new_value


def is_app_assignment(node):
    if not isinstance(node.body[0], Assign):
        return False

    target = node.body[0].targets[0].target

    if not isinstance(target, Attribute):
        return False

    if not (target.value.value == 'self' and target.attr.value == '_app'):
        return False

    return True
