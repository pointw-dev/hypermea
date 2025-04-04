import pytest
from pytest_bdd import scenario, given, when, then

from tests.hypermea import *
from tests.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Sorting can be disabled globally')
def test_sorting_can_be_disabled_globally():
    pass


# Given sorting is disabled globally
# And a resource is configured
# And that resource has multiple items in its collection
# When a client requests this collection with a sort query string

@then('the collection in the response is not sorted')
def then_the_collection_in_the_response_is_not_sorted(context):
    names = [i['name'] for i in context.people]
    is_sorted = all([True if index == 0 else item >= names[index-1] for index, item in enumerate(names)])
    assert_that(is_sorted).is_equal_to(False)
