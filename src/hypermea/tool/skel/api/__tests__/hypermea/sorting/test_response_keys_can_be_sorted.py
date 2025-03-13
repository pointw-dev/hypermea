import pytest
from pytest_bdd import scenario, given, when, then
from __tests__.hypermea.sorting import *


@pytest.fixture(scope='module')
def context():
    return {}


@scenario(FEATURE_PATH, "An item's keys can be sorted")
def test_response_keys_can_be_sorted():
    pass


@given('key sorting is enabled')
def step_impl(eve_settings):
    eve_settings['JSON_SORT_KEYS'] = True


@given('a resource is configured with multiple keys')
def step_impl(eve_settings):
    eve_settings['DOMAIN'] = {
        'widgets': {
            'schema': {
                'name': {'type': 'string'},
                'chain': {'type': 'string'},
                'significance': {'type': 'string'},
                'score': {'type': 'string'}
            }
        }
    }


@given('that resource has an item in its collection')
def step_impl(api, context):
    widget = {
        'name': 'value',
        'chain': 'value',
        'significance': 'value',
        'score': 'value'
    }
    response = api.post('/widgets', data=json.dumps(widget), content_type='application/json')
    assert_that(response.status_code).is_equal_to(201)
    context['widget_id'] = response.json['_id']


@when('a client requests that resource')
def step_impl(api, context):
    response = api.get(f'/widgets/{context["widget_id"]}')
    assert_that(response.status_code).is_equal_to(200)
    context['widget'] = response.json


@then('the keys are sorted in the response')
def step_impl(context):
    keys = list(context['widget'].keys())
    is_sorted = all([True if index == 0 else item >= keys[index - 1] for index, item in enumerate(keys)])
    assert_that(is_sorted).is_equal_to(True)
