import pytest
from pytest_bdd import scenario, given, when, then
from tests.hypermea import *
from tests.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, "An item's keys can be sorted")
def test_response_keys_can_be_sorted():
    pass


@given('key sorting is enabled')
def given_key_sorting_is_enabled(dev_time_settings):
    dev_time_settings['JSON_SORT_KEYS'] = True

# Given a resource is configured with multiple keys
# Given that resource has an item in its collection

@when('a client requests that resource')
def when_a_client_requests_that_resource(api, context):
    response = api.get(f'/widgets/{context.widget_id}')
    assert_that(response.status_code).is_equal_to(200)
    context.widget = response.json


@then('the keys are sorted in the response')
def then_the_keys_are_sorted_in_the_response(context):
    keys = list(context.widget.keys())
    is_sorted = all([True if index == 0 else item >= keys[index - 1] for index, item in enumerate(keys)])
    assert_that(is_sorted).is_equal_to(True)
