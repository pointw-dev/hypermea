import pytest
from pytest_bdd import given, when, then, parsers
from assertpy import assert_that
from pytest_mock import mocker
import smtplib

from tests.hypermea import *
from tests.hypermea.enhanced_logging import *


@pytest.fixture(scope='function')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Log entries can be sent by email')
def SKIP_test_logged_error_entries_are_sent_by_email():
    pass


@given(parsers.parse('the service is configured to send emails on {verbosity} logs'))
def given_the_service_is_configured_to_use_an_smtp_server(mocker, deploy_time_settings, context, verbosity):
    smtp_mock_name = 'smtplib.SMTP'
    context.mock_smtp = mocker.MagicMock(name=smtp_mock_name)
    mocker.patch(smtp_mock_name, new=context.mock_smtp)

    deploy_time_settings.smtp.host = 'mail.example.com'

    deploy_time_settings.logging.log_to_email = True
    deploy_time_settings.logging.log_email_from = f'{deploy_time_settings.hypermea.service_name} <no-reply@example.com>'
    deploy_time_settings.logging.log_email_recipients = 'michael@example.com'
    deploy_time_settings.logging.log_email_verbosity = verbosity
    deploy_time_settings.logging.add_echo = True


@when(parsers.parse('a {level} entry is logged'))
def when_a_level_entry_is_logged(api, level):
    status_code = 200
    if level == 'ERROR':
        status_code = 500
    elif level == 'WARNING':
        status_code = 400

    echo = {
        'status_code': status_code,
        'message': f'Testing with level {level}'
    }
    api.put('/_echo', data=json.dumps(echo), headers={'Content-Type': 'application/json'})


@then(parsers.parse('the number of emails sent will be {expected:d}'))
def then_the_number_of_emails_sent_will_be_expected(context, expected):
    actual_calls = context.mock_smtp.return_value.send_message.call_count
    assert_that(actual_calls).is_equal_to(expected)
