import pytest
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pytest_bdd import given, when, then, parsers
from __tests__.hypermea import *
from __tests__.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return {}


@annotated_scenario(FEATURE_PATH, 'Embedded section does appear for child item when requested')
def test_embedded_section_does_appear_for_child_item_when_requested():
    pass


@when('a client requests a child item asking for related parent')
def step_impl(api, context):
    result = api.get(f"/cars/{context['first_car_id']}?embed=person")
    assert_that(result.status_code).is_equal_to(200)
    context['car'] = result.json

@then("the child's parent item appears in embedded property")
def step_impl(context):
    assert_that(context['car']).contains_key('_embedded')
    assert_that(context['car']['_embedded']).contains_key('person')
    assert_that(context['car']['_embedded']['person']).is_type_of(dict)
