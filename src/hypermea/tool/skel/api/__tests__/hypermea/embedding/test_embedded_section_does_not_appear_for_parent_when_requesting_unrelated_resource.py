import pytest
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from pytest_bdd import given, when, then, parsers
from __tests__.hypermea import *
from __tests__.hypermea.embedding import *


@pytest.fixture(scope='module')
def context():
    return {}


@annotated_scenario(FEATURE_PATH, 'Embedded section does not appear for parent when requesting unrelated resource')
def test_embedded_section_does_not_appear_for_parent_when_requesting_unrelated_resource():
    pass


@when('a client requests a parent item with an unrelated resource')
def step_impl(api, context):
    result = api.get(f"/people/{context['first_person_id']}?embed=unrelated")
    assert_that(result.status_code).is_equal_to(200)
    context['person'] = result.json

