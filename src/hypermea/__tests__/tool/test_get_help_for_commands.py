from pytest_bdd import scenario, given, when, then, parsers
from __tests__.terminal_harness import TerminalHarness
from __tests__.tool import FEATURE


@scenario(FEATURE, 'Get help for commands')
def test_get_help_for_commands():
    pass


@given('I am at a terminal', target_fixture='context')
def context():
    context.terminal = TerminalHarness()
    return context


@when(parsers.parse('I request help for the {command} command'))
def request_help_for_a_command(context, command):
    context.terminal.run(f'hy {command} --help')


@then(parsers.parse('the console displays help information for that {command}'))
def check_console(context, command):
    context.terminal.console.displays(f'Usage: hy {command}')
