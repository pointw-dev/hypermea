import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedded section does not appear for parent when requesting unrelated resource')
def test_embedded_section_does_not_appear_for_parent_when_requesting_unrelated_resource():
    pass


@when('a client requests a parent item with an unrelated resource')
def when_a_client_requests_a_parent_item_with_an_unrelated_resource(api, context):
    response = api.get(f"/people/{context.first_person_id}?embed=unrelated")
    assert_that(response.status_code).is_equal_to(200)
    context.resource = response.json

