import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedded section does appear for child item when requested')
def test_embedded_section_does_appear_for_child_item_when_requested():
    pass


@then("the child's parent item appears in embedded property")
def then_the_childs_parent_item_appears_in_embedded_property(context):
    assert_that(context.resource).contains_key('_embedded')
    assert_that(context.resource['_embedded']).contains_key('people')
    assert_that(context.resource['_embedded']['people']).is_type_of(dict)
