import pytest
from pytest_bdd import scenario, given, when, then

from tests.hypermea import *
from tests.hypermea.pretty_printing import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Client requests a resource without pretty-printing')
def test_resource_is_not_pretty_printed_by_default():
    pass


# Given a resource is configured
# And that resource has an item in its collection

@when('a client requests that resource without pretty printing')
def when_a_client_requests_that_resource_without_pretty_printing(api, context):
    response = api.get(f'/widgets/{context.widget_id}')
    assert_that(response.status_code).is_equal_to(200)
    context.widget = response.data.decode('utf-8')


@then('the response is not pretty-printed')
def then_the_response_is_not_prettyprinted(context):
    assert_that(getattr(context, 'widget', None).count('\n')).is_equal_to(0)
