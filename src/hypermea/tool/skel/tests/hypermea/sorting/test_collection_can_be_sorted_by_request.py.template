import pytest
from pytest_bdd import scenario, given, when, then

from tests import annotated_scenario
from tests.hypermea import *
from tests.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Client can sort collections using the sort query string parameter')
def test_collection_can_be_sorted_by_request():
    pass

# Given a resource is configured
# And that resource has multiple items in its collection
# When a client requests this collection with a sort query string
# Then the collection in the response is sorted accordingly
