import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Child resource collections are embedded by default')
def test_child_resource_collections_are_embedded_by_default():
    pass


@when('a client requests the children of a parent')
def when_a_client_requests_the_children_of_a_parent(api, context):
    response = api.get(f"/people/{context.first_person_id}/cars")
    assert_that(response.status_code).is_equal_to(200)
    context.collection = response.json
    context.rel = 'cars'
