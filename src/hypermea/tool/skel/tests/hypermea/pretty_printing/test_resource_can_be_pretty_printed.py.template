import pytest
from types import SimpleNamespace
from pytest_bdd import given, when, then, parsers

from tests import *
from tests.hypermea import *
from tests.hypermea.pretty_printing import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Client can request a pretty-printed resource')
def test_resource_can_be_pretty_printed():
    pass

# Given a resource is configured
# And that resource has an item in its collection

@when('a client requests that resource with pretty printing')
def when_a_client_requests_that_resource_with_pretty_printing(api, context):
    response = api.get(f'/widgets/{context.widget_id}?pretty')
    assert_that(response.status_code).is_equal_to(200)
    context.widget = response.data.decode('utf-8')

@then('the response is pretty-printed')
def then_the_response_is_prettyprinted(context):
    assert_that(getattr(context, 'widget', None).count('\n')).is_greater_than(5)
