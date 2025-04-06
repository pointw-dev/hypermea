import pytest
from pytest_bdd import given, when, then, parsers
from tests.hypermea import *
from tests.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return SimpleNamespace()


@annotated_scenario(FEATURE, 'Embedded collection comes with pagination controls if larger than configured limit')
def test_embedded_collection_comes_with_pagination_controls_if_larger_than_configured_limit():
    pass


@then('the parent links contain page controls for the embedded child collection')
def then_the_parent_links_contain_page_controls_for_the_embedded_child_collection(context):
    links = context.resource['_links']
    assert_that(links).contains_key('cars:next')
    assert_that(links).described_as('will fail if OPTIMIZE_PAGINATION_FOR_SPEED is True').contains_key('cars:last')
