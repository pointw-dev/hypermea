import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Parent resource collections are embedded by default')
def test_parent_collections_are_embedded_by_default():
    pass

# Background:
#   Given a parent and a child resource are configured
#   And each resource has multiple items

@when('a client requests the parent resource collection')
def when_a_client_requests_the_parent_resource_collection(api, context):
    response = api.get('/people')
    assert_that(response.status_code).is_equal_to(200)
    context.collection = response.json
    context.rel = 'people'
