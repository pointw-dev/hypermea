import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.pagination import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Client can limit the number of items in a collection')
def test_client_can_limit_items_returned_in_a_collection():
    pass

# Given a resource is configured
# And that resource has 100 items in its collection
# When a client requests this collection with a limit of <limit>
# Then the collection in the response has <limit> items
# And the next link relation is <next_link>
# And the value of the last page is <last_page>
