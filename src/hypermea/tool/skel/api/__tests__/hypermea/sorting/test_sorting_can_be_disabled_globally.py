import pytest
from pytest_bdd import scenario, given, when, then

from __tests__.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Sorting can be disabled globally')
def test_collection_can_be_sorted_by_request():
    pass


# Given sorting is disabled globally
# And a resource collection exists
# And a resource has multiple items in its collection
# When a client requests this collection with a sort query string

@then('the collection in the response is not sorted')
def step_impl(context):
    names = [i['name'] for i in context['people']]
    is_sorted = all([True if index == 0 else item >= names[index-1] for index, item in enumerate(names)])
    assert_that(is_sorted).is_equal_to(False)
