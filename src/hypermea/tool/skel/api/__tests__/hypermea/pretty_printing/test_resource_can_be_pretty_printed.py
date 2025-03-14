import pytest
from assertpy import assert_that
from pytest_bdd import scenario, given, when, then
from __tests__.hypermea import *
from __tests__.hypermea.pretty_printing import *




@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Client can request a pretty-printed resource')
def test_resource_can_be_pretty_printed():
    pass


# Given a resource is configured
# And that resource has an item in its collection

@when('a client requests that resource with pretty printing')
def step_impl(api, context):
    response = api.get(f'/widgets/{context["widget_id"]}?pretty')
    assert_that(response.status_code).is_equal_to(200)
    context['widget'] = response.data.decode('utf-8')

@then('the response is pretty-printed')
def step_impl(context):
    assert_that(context.get('widget').count('\n')).is_equal_to(23)
