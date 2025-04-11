import os
import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.enhanced_logging import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Choose the folder to log to')
def SKIP_test_choose_the_folder_to_log_to():
    pass


@given('the log folder is specified')
def given_the_log_folder_is_specified(deploy_time_settings):
    deploy_time_settings.logging.folder_to_log_to = '/some/folder'


@then('the log is written to the specified location')
def then_the_log_is_written_to_the_specified_location():
    log_exists = os.path.isfile(f'/some/folder/all.log')
    assert_that(log_exists).is_true()
