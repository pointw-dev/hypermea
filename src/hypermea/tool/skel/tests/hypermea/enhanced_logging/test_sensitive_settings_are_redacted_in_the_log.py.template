import pytest
from pydantic import SecretStr
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from tests.hypermea import *
from tests.hypermea.enhanced_logging import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Sensitive settings are redacted in the log')
def test_sensitive_settings_are_redacted_in_the_log():
    pass


@given('I have configured a setting for a password')
def given_i_have_configured_a_setting_for_a_password(deploy_time_settings):
    deploy_time_settings.mongo.username = ''
    deploy_time_settings.mongo.password = SecretStr('swordfish')


@then('I do not see the secret values')
def then_i_do_not_see_the_secret_values(context):
    deploy_time_settings = [entry for entry in context.log_entries if entry[0] == 'service' and entry[2].startswith('HY_')]
    assert_that(len(deploy_time_settings)).is_greater_than(0)

    log_string = ''.join(str(context.log_entries))

    assert_that(log_string).contains('MONGO_PASSWORD')
    assert_that(log_string).does_not_contain('swordfish')
