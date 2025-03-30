import pytest
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pytest_bdd import given, when, then, parsers
from __tests__.hypermea import *
from __tests__.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return {}


@annotated_scenario(FEATURE_PATH, 'Embedded section does not appear for child item when not requested')
def test_embedded_section_does_not_appear_for_child_item_when_not_requested():
    pass


@when('a client requests a child item without asking for related parent')
def step_impl(api, context):
    result = api.get(f"/cars/{context['first_car_id']}")
    assert_that(result.status_code).is_equal_to(200)
    context['car'] = result.json
