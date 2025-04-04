import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedded section does not appear for child item when not requested')
def test_embedded_section_does_not_appear_for_child_item_when_not_requested():
    pass


@when('a client requests a child item without asking for related parent')
def when_a_client_requests_a_child_item_without_asking_for_related_parent(api, context):
    response = api.get(f"/cars/{context.first_car_id}")
    assert_that(response.status_code).is_equal_to(200)
    context.resource = response.json
