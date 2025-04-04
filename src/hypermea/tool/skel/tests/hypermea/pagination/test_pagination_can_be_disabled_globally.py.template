import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Pagination can be disabled globally')
def test_pagination_can_be_disabled_globally():
    pass

# Given pagination is disabled globally
# And a resource is configured
# And that resource has 100 items in its collection
# When a client requests this collection with a limit of <limit>

@then('the limit part of the request is ignored')
def then_the_limit_part_of_the_request_is_ignored(context):
    next_link = 'present' if 'next' in context.people['_links'] else 'absent'
    prev_link = 'present' if 'prev' in context.people['_links'] else 'absent'
    last_link = 'absent' if 'last' not in context.people['_links'] else context.people['_links']['last']['href']
    meta = 'absent' if '_meta' not in context.people else 'absent'
    assert_that(next_link).is_equal_to('absent')
    assert_that(prev_link).is_equal_to('absent')
    assert_that(last_link).is_equal_to('absent')
    assert_that(meta).is_equal_to('absent')


