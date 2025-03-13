import pytest
from pytest_bdd import scenario, given, when, then

from __tests__.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Client can sort collections using the sort query string parameter')
def test_collection_can_be_sorted_by_request():
    pass

# Given a resource collection exists
# And a resource has multiple items in its collection

@when("a client requests this collection with a sort query string")
def step_impl(api, context):
    response = api.get(
        '/people?sort=name',
        headers={'content-type': 'application/json'}
    )
    assert_that(response.status_code).is_equal_to(200)
    context['people'] = response.json['_items']

# Then the collection in the response is sorted accordingly
