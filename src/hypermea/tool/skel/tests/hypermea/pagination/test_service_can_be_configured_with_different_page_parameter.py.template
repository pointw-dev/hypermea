import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Service can be configured with a different page query string parameter')
def test_service_can_be_configured_with_different_page_parameter():
    pass


@given("the service is configured with a different page query string parameter")
def given_the_service_is_configured_with_a_different_page_query_string_parameter(dev_time_settings):
    dev_time_settings['QUERY_PAGE'] = 'pg'

# And a resource is configured
# And that resource has 100 items in its collection

@when("a client requests this collection using the new page parameter")
def when_a_client_requests_this_collection_using_the_new_page_parameter(api, context):
    response = api.get(
        f'/people?max_results&pg=2',
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json


@then("the collection in the response contains the correct page")
def then_the_collection_in_the_response_contains_the_correct_page(context):
    meta = context.people['_meta']
    assert_that(meta['pg']).is_equal_to(2)
