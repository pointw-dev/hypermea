import pytest
from pytest_bdd import scenario, given, when, then
from tests.hypermea import *
from tests.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Service can be configured with a different sort query string parameter')
def test_sort_parameter_name_can_be_changed():
    pass


@given('the service is configured with a different sort query string parameter')
def given_the_service_is_configured_with_a_different_sort_query_string_parameter(dev_time_settings):
    dev_time_settings['QUERY_SORT'] = 'order_by'

# And a resource is configured
# And that resource has multiple items in its collection

@when('a client requests this collection using the new sort parameter')
def when_a_client_requests_this_collection_using_the_new_sort_parameter(api, context):
    response = api.get(
        '/people?order_by=name'
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json['_embedded']['people']

# Then the collection in the response is sorted accordingly
