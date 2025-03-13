import pytest
from assertpy import assert_that
from pytest_bdd import scenario, given, when, then
from __tests__.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, 'Service can be configured with a different sort query string parameter')
def test_authenticated_users_can_add_notes():
    pass


@given('an eve setting is set this way')
def step_impl(eve_settings):
    # eve_settings['DOMAIN'] = {'_settings': {'resource_methods': ['GET'], 'schema': {}}, 'cars': {'additional_lookup': {'field': 'name', 'url': 'regex("[\w]+")'}, 'datasource': {'projection': {'_tenant': 0}}, 'schema': {'_person_ref': {'data_relation': {'embeddable': True, 'resource': 'people'}, 'type': 'objectid'}, '_tags': {'schema': {'type': 'string'}, 'type': 'list'}, '_tenant': {'type': 'string'}, '_x': {'allow_unknown': True}, 'description': {'type': 'string'}, 'name': {'empty': False, 'required': True, 'type': 'string', 'unique': True}}}, 'people': {'additional_lookup': {'field': 'name', 'url': 'regex("[\w]+")'}, 'datasource': {'projection': {'_tenant': 0}}, 'schema': {'_tags': {'schema': {'type': 'string'}, 'type': 'list'}, '_tenant': {'type': 'string'}, '_x': {'allow_unknown': True}, 'description': {'type': 'string'}, 'name': {'empty': False, 'required': True, 'type': 'string', 'unique': True}}}, 'people_cars': {'datasource': {'source': 'cars'}, 'resource_title': 'cars', 'schema': {'_person_ref': {'data_relation': {'embeddable': True, 'resource': 'people'}, 'type': 'objectid'}, '_tags': {'schema': {'type': 'string'}, 'type': 'list'}, '_tenant': {'type': 'string'}, '_x': {'allow_unknown': True}, 'description': {'type': 'string'}, 'name': {'empty': False, 'required': True, 'type': 'string', 'unique': True}}, 'url': 'people/<regex("[a-f0-9]{24}"):_person_ref>/cars'}}
    eve_settings['DOMAIN'] = {'contacts': {}}
    pass

@given('a hypermea setting is set that way')
def step_impl(hypermea_settings):
    # hypermea_settings['HY_API_PORT'] = '2112'
    pass


@given("a resource has multiple items in its collection")
def step_impl(api):
    response = api.get('/')
    assert_that(response.status_code).is_equal_to(200)


@when("a client requests this collection")
def step_impl():
    pass


@when("provides a sort query string")
def step_impl():
    pass


@then("the collection in the response is sorted accordingly")
def step_impl():
    pass