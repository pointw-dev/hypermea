from pytest_bdd import given, when, then, parsers
from tests import *
from tests.hypermea import *

FEATURE = 'hypermea/delete_response.feature'


@when('a client deletes all items in a resource collection')
def when_a_client_deletes_all_items_in_a_resource_collection(api, context):
    context.response = api.delete(f'/people')

@then(parsers.parse('the response status code is {expected_status_code:d}'))
def then_the_response_has_expected_status_code(context, expected_status_code):
    assert_that(context.response.status_code).is_equal_to(expected_status_code)

@then(parsers.parse('the response body has a delete count of {expected_delete_count:d}'))
def then_the_response_body_has_a_expected_delete(context, expected_delete_count):
    assert_that(context.response.json.get('delete_count')).is_equal_to(expected_delete_count)

@then('the response body has links with the following')
def then_the_response_body_has_expected_links(context, datatable):
    links = context.response.json.get('_links', {})
    for row in datatable[1:]:  # peel off the header row
        rel, = row
        assert_that(links).contains_key(rel)
