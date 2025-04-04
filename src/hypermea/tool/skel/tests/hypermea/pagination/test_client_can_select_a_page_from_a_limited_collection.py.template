import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Client can request a page in a limited collection')
def test_client_can_select_a_page_from_a_limited_collection():
    pass

# Given a resource is configured
# And that resource has 100 items in its collection

@when(parsers.parse('a client requests page {page} of this collection with a limit of {limit:d}'))
def when_a_client_requests_page_page_of_this_collection_with_a_limit_of_limit(api, context, page, limit):
    response = api.get(
        f'/people?max_results={limit}&page={page}'
    )
    assert_that(response.status_code).is_equal_to(200)
    context.people = response.json

# Then the collection in the response has <limit> items
# And the next link relation is <next_link>
# And the value of the last page is <last_page>
