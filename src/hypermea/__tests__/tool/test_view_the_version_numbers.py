from pytest_bdd import scenario, given, when, then, parsers
from assertpy import assert_that  # https://github.com/assertpy/assertpy
from __tests__.tool import FEATURE
from __tests__.tool.terminal_harness import TerminalHarness


@scenario(FEATURE, 'View the version numbers')
def test_view_the_version_numbers():
    pass

@given('I am at a terminal', target_fixture='context')
def context():
    context.terminal = TerminalHarness()
    return context


@when('I request the hypermea version')
def request_hypermea_version(context):
    context.terminal.run('hy --version')
#    context.terminal.run('echo hypermea-core')


@then('the console displays the version number for both core and tool')
def check_console(context):
    context.terminal.console.displays('hypermea-core')

