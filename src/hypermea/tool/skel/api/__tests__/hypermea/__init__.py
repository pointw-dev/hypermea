import json
from assertpy import assert_that
from pytest_bdd import scenario, given, when, then


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


