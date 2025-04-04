import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedded section does appear for parent item when requested')
def test_embedded_section_does_appear_for_parent_item_when_requested():
    pass


#   When a client requests a parent item asking for related children
#   Then the parent's children appear in embedded property

@then("the parent's children appear in embedded property")
def then_the_parents_children_appear_in_embedded_property(context):
    assert_that(context.resource).contains_key('_embedded')
    assert_that(context.resource['_embedded']).contains_key('cars')
    assert_that(context.resource['_embedded']['cars']).is_type_of(list)
