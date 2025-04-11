import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()

LIMIT = 5

@annotated_scenario(FEATURE, 'Service can be configured with a different limit query string parameter')
def test_service_can_be_configured_with_different_limit_parameter():
    pass


@given("the service is configured with a different limit query string parameter")
def given_the_service_is_configured_with_a_different_limit_query_string_parameter(dev_time_settings):
    dev_time_settings['QUERY_MAX_RESULTS'] = 'limit'

# And a resource is configured
# And that resource has 100 items in its collection

@when("a client requests this collection using the new limit parameter")
def when_a_client_requests_this_collection_using_the_new_limit_parameter(api, context):
    response = api.get(
        f'/people?limit={LIMIT}',
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json


@then("the collection in the response is limited accordingly")
def then_the_collection_in_the_response_is_limited_accordingly(context):
    item_count = len(context.people['_embedded']['people'])
    assert_that(item_count).is_equal_to(LIMIT)
