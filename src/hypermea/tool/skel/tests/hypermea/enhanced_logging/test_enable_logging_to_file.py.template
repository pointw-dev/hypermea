import os.path
import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.enhanced_logging import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Enable logging to file')
def SKIP_test_enable_logging_to_file():
    pass


@then('the log is written to the default location')
def then_the_log_is_written_to_the_default_location():
    service_name = settings.hypermea.service_name
    log_exists = os.path.isfile(f'/var/log/{service_name}/all.log')
    assert_that(log_exists).is_true()
