from pytest_bdd import given, when, then, parsers
from tests import *
from tests.hypermea import *


FEATURE = 'hypermea/sorting.feature'


@given('sorting is disabled globally')
def given_sorting_is_disabled_globally(dev_time_settings):
    dev_time_settings['SORTING'] = False


# shared When step definitions
@when('a client requests this collection with a sort query string')
def when_a_client_requests_this_collection_with_a_sort_query_string(api, context):
    response = api.get(
        '/people?sort=name'
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json['_embedded']['people']


# shared Then step definitions
@then('the collection in the response is sorted accordingly')
def then_the_collection_in_the_response_is_sorted_accordingly(context):
    names = [i['name'] for i in context.people]
    is_sorted = all([True if index == 0 else item >= names[index-1] for index, item in enumerate(names)])
    assert_that(is_sorted).is_equal_to(True)
