import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedding in a collection')
def test_embedding_in_a_collection():
    pass


@when('a client requests the parent collection asking for embedded children')
def when_a_client_requests_the_parent_collection_asking_for_embedded_children(api, context):
    response = api.get('/people?embed=cars')
    assert_that(response.status_code).is_equal_to(200)
    context.collection = response.json
    context.rel = 'people'


@then("each item in the embedded parent collection must contain that parent's children")
def then_each_item_in_the_embedded_parent_collection_must_contain_that_parents_children(context):
    for person in context.collection['_embedded']['people']:
        assert_that(person['_embedded']).contains_key('cars')
        assert_that(person['_embedded']['cars']).is_type_of(list)
