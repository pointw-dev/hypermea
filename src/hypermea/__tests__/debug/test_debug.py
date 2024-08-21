import os
import shutil
from pytest_bdd import scenario, given, when, then, parsers
from __tests__.terminal_harness import TerminalHarness
from __tests__.debug import FEATURE


@scenario(FEATURE, 'Writes a file to the filesystem')
def test_get_help_for_commands():
    pass


@given('I am at a terminal', target_fixture='context')
def context():
    context.terminal = TerminalHarness()
    return context


@given('I am in an empty directory')
def i_am_in_an_empty_directory():
    # if path exists, remove it even it contains files
    if os.path.exists('__toxtest__'):
        shutil.rmtree('__toxtest__')
    os.mkdir('__toxtest__')
    os.chdir('__toxtest__')


@when('I write a file to the filesystem')
def request_help_for_a_command(context):
    context.terminal.run(f'hy setting create')


@then('the file contains the string "Hello, World!"')
def check_console(context):
    with open('schnizzel.txt', 'r') as file:
        content = file.read()
    assert 'Hello, world!\n' in content, f"Expected 'Hello, world!\n' to be in file content"
