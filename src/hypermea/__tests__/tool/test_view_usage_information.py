from pytest_bdd import scenario, given, when, then, parsers
from __tests__.tool import FEATURE
from __tests__.tool.terminal_harness import TerminalHarness


@scenario(FEATURE, 'View the usage information')
def test_view_the_usage_information():
    pass


@given('I am at a terminal', target_fixture='context')
def context():
    context.terminal = TerminalHarness()
    return context


@when('I run hypermea with no parameters')
def run_with_no_parameters(context):
    context.terminal.run('hy')


@then('the console displays usage information')
def check_console(context):
    context.terminal.console.displays('Usage: ')

