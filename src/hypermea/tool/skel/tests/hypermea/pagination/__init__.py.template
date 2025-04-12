from urllib.parse import urlparse, parse_qsl
from pytest_bdd import given, when, then, parsers
from tests import *
from tests.hypermea import *

FEATURE = 'hypermea/pagination.feature'


@given(parsers.parse('that resource has {number_of_items:d} items in its collection'))
def given_that_resource_has_numberofitems_items_in_its_collection(api, number_of_items):
    people = []
    for index in range(number_of_items):
        people.append({'name': f'name{index+1}'})
    response = api.post(
        '/people',
        data=json.dumps(people),
        headers={'content-type': 'application/json'}
    )
    assert_that(response.status_code).is_equal_to(201)


@given('pagination is disabled globally')
def given_pagination_is_disabled_globally(dev_time_settings):
    dev_time_settings['PAGINATION'] = False

@given(parsers.parse('the service is configured to limit page sizes to {limit:d}'))
def given_the_service_is_configured_to_limit_page_sizes_to_100(deploy_time_settings, limit):
    deploy_time_settings.hypermea.pagination_limit = limit


@when('a client requests this resource with no pagination controls')
def given_a_client_requests_this_resource_with_no_pagination_controls(api, context):
    response = api.get(
        f'/people',
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json


@when(parsers.parse('a client requests this collection with a limit of {limit:d}'))
def when_a_client_requests_this_collection_with_a_limit_of_limit(api, context, limit):
    response = api.get(
        f'/people?max_results={limit}',
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json


@then(parsers.parse('the collection in the response has {limit:d} items'))
def then_the_collection_in_the_response_has_limit_items(context, limit):
    item_count = len(context.people['_embedded']['people'])
    if limit > item_count:
        limit = item_count
    assert_that(item_count).is_equal_to(limit)


@then(parsers.parse('the next link relation is {next_link}'))
def then_the_next_link_relation_is_nextlink(context, next_link):
    actual_next_link = 'present' if 'next' in context.people['_links'] else 'absent'
    assert_that(actual_next_link).is_equal_to(next_link)


@then(parsers.parse('the prev link relation is {prev_link}'))
def then_the_prev_link_relation_is_prevlink(context, prev_link):
    actual_prev_link = 'present' if 'prev' in context.people['_links'] else 'absent'
    assert_that(actual_prev_link).is_equal_to(prev_link)


@then(parsers.parse('the value of the last page is {last_page}'))
def then_the_value_of_the_last_page_is_lastpage(context, last_page):
    last_link = 'absent' if 'last' not in context.people['_links'] else context.people['_links']['last']['href']
    if last_link == 'absent':
        actual_last_page = 'absent'
    else:
        parsed = urlparse(last_link)
        query_params = parse_qsl(parsed.query, keep_blank_values=True)
        actual_last_page = next((value for key, value in query_params if key == 'page'), 'absent')
    assert_that(actual_last_page).described_as('will fail if OPTIMIZE_PAGINATION_FOR_SPEED is True').is_equal_to(last_page)
